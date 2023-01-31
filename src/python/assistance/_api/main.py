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

import json
import logging

import uvicorn
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse

from assistance import _ctx
from assistance._config import get_google_oauth_client_id
from assistance._keys import (
    get_google_oauth_client_secret,
    get_starlette_session_key,
    set_openai_api_key,
)

from .routers import chat, query, root, save, search, send, summarise

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=get_starlette_session_key())

origins = [
    "https://assistance.chat",
    "https://*.assistance.chat",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(chat.router)
# app.include_router(save.router)
# app.include_router(search.router)
# app.include_router(send.router)
# app.include_router(summarise.router)
# app.include_router(query.router)


@app.on_event("startup")
async def startup_event():
    set_openai_api_key()
    _ctx.open_session()


@app.on_event("shutdown")
async def shutdown_event():
    await _ctx.close_session()


def main():
    uvicorn.run("assistance._api.main:app", port=8000, log_level="info", reload=True)


if __name__ == "__main__":
    main()
