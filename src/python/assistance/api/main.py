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
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from . import ctx
from .conversations import (
    call_gpt_and_store_as_transcript,
    run_career_chat_response,
    run_career_chat_start,
)
from .keys import set_openai_api_key
from .login import (
    Token,
    User,
    create_temp_account,
    get_current_user,
    get_user_access_token,
)
from .mailgun import send_access_link
from .search import alphacrucis_search
from .store import store_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


app = FastAPI()

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


@app.post("/login", response_model=Token)
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = get_user_access_token(form_data.username, form_data.password)

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/temp-account")
async def temp_account():
    username = create_temp_account()

    return {"username": username}


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


class ChatStartData(BaseModel):
    client_name: str
    agent_name: str
    prompt: str


@app.post("/chat/career/start")
@app.post("/chat/start")
async def career_chat_start(
    data: ChatStartData,
    current_user: User = Depends(get_current_user),
):
    response = await run_career_chat_start(
        username=current_user.username,
        client_name=data.client_name,
        agent_name=data.agent_name,
        prompt=data.prompt,
    )

    return {"response": response}


class ChatContinueData(BaseModel):
    client_name: str
    agent_name: str
    client_text: str


@app.post("/chat/career/start")
@app.post("/chat/continue")
async def career_chat_continue(
    data: ChatContinueData,
    current_user: User = Depends(get_current_user),
):
    response = await run_career_chat_response(
        username=current_user.username,
        client_name=data.client_name,
        agent_name=data.agent_name,
        client_text=data.client_text,
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


class StoreData(BaseModel):
    record_grouping: str
    content: str


@app.post("/save/form")
async def save_form(
    data: StoreData,
    current_user: User = Depends(get_current_user),
):
    dirnames = [data.record_grouping, current_user.username, "forms"]
    filename = "form.txt"

    await store_file(dirnames=dirnames, filename=filename, contents=data.content)


class SearchData(BaseModel):
    record_grouping: str
    query: str


@app.post("/search/alphacrucis")
async def run_alphacrucis_search(
    data: SearchData,
    _current_user: User = Depends(get_current_user),
):
    result = await alphacrucis_search(query=data.query)

    return result


@app.post("/send/signin-link")
async def send_user_signin_link(email: str):
    await send_access_link(email=email)


def main():
    uvicorn.run("assistance.api.main:app", port=8080, log_level="info", reload=True)


if __name__ == "__main__":
    main()
