# Copyright (C) 2022 Assistance.Chat contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import aiohttp
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from assistance import ctx
from assistance.conversations import call_gpt_and_store_as_transcript
from assistance.keys import set_openai_api_key
from assistance.mailgun import send_access_link
from assistance.store import store_file

from . import chat, save, search
from .login import login
from .login.utilities import User, get_current_user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


app = FastAPI()

app.include_router(chat.router)
app.include_router(save.router)
app.include_router(login.router)
app.include_router(search.router)

origins = [
    "https://career.assistance.chat",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://10.0.0.117:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    set_openai_api_key()
    ctx.session = aiohttp.ClientSession()


@app.on_event("shutdown")
async def shutdown_event():
    await ctx.session.close()


class Prompt(BaseModel):
    record_grouping: str
    model_kwargs: dict
    prompt: str


@app.post("/prompt")
async def run_prompt(
    data: Prompt,
    current_user: User = Depends(get_current_user),
):
    response = await call_gpt_and_store_as_transcript(
        record_grouping=data.record_grouping,
        username=current_user.username,
        model_kwargs=data.model_kwargs,
        prompt=data.prompt,
    )

    return {"response": response}


class StoreDataRecordGroupingOptional(BaseModel):
    record_grouping: str | None = None
    content: str


@app.post("/save")
async def save_content(
    data: StoreDataRecordGroupingOptional,
    current_user: User = Depends(get_current_user),
):
    record_grouping = data.record_grouping

    if record_grouping is None:
        record_grouping = "career.assistance.chat"

    dirnames = [record_grouping, current_user.username, "save-api-call"]
    filename = "contents.txt"

    await store_file(dirnames=dirnames, filename=filename, contents=data.content)


@app.post("/send/signin-link")
async def send_user_signin_link(email: str):
    await send_access_link(email=email)


def main():
    uvicorn.run("assistance.api.main:app", port=8080, log_level="info", reload=True)


if __name__ == "__main__":
    main()
