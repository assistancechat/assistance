# Copyright (C) 2023 Assistance.Chat contributors

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

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from pydantic import BaseModel
from starlette.config import Config
from starlette.responses import HTMLResponse, RedirectResponse

from assistance._config import get_google_oauth_client_id
from assistance._keys import get_google_oauth_client_secret

router = APIRouter(prefix="")

# OAuth implementation built based on the official demo oath client
# that has been forked at the following location:
# https://github.com/assistancechat/demo-oauth-client/blob/e9c8aa1c9d05da32c8ca0a740b6475c78b53e6c6/fastapi-google-login/app.py
oauth = OAuth(
    Config(
        environ={
            "GOOGLE_CLIENT_ID": get_google_oauth_client_id(),
            "GOOGLE_CLIENT_SECRET": get_google_oauth_client_secret(),
        }
    )
)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/")
async def homepage(request: Request):
    user = request.session.get("user")
    if user:
        data = json.dumps(user)
        html = f"<pre>{data}</pre>" '<a href="/logout">logout</a>'
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f"<h1>{error.error}</h1>")
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
    return RedirectResponse(url="/")


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


class Prompt(BaseModel):
    record_grouping: str
    model_kwargs: dict
    prompt: str
