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

import asyncio
import logging
from datetime import datetime, timedelta
from typing import NamedTuple, TypedDict
from urllib.parse import urlparse

from google.auth import exceptions
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import BaseModel

from assistance._agents.conversations import run_conversation
from assistance._api.exceptions import CredentialsException
from assistance._config import get_google_oauth_client_id
from assistance._keys import get_jwt_key, get_openai_api_key

GOOGLE_OAUTH_CLIENT_ID = get_google_oauth_client_id()

JWT_SECRET_KEY = get_jwt_key()
OPENAI_API_KEY = get_openai_api_key()

ALGORITHM = "HS256"
ASSISTANCE_TOKEN_EXPIRES = timedelta(minutes=30)
ASSISTANCE_TOKEN_REFRESH = timedelta(minutes=10)


class ChatData(BaseModel):
    client_email: str | None = None
    client_name: str | None = None
    agent_name: str
    task_prompt: str
    transcript: str | None = None
    google_id_token: str | None = None
    assistance_token: str | None = None
    openai_api_key: str | None = None


class ChatResponse(BaseModel):
    agent_message: str
    assistance_token: str


async def run_chat(data: ChatData, origin_url: str) -> ChatResponse:
    # TODO: Sort data storage by origin_url
    logging.info(origin_url)

    openai_api_key = data.openai_api_key
    use_client_openai_api_key = openai_api_key is not None

    (
        assistance_token,
        assistance_token_data,
    ) = await _verify_and_get_assistance_token_with_data(
        google_id_token=data.google_id_token,
        assistance_token=data.assistance_token,
        use_client_openai_api_key=openai_api_key is not None,
    )

    assert (
        assistance_token_data["use_client_openai_api_key"] == use_client_openai_api_key
    )

    client_email = assistance_token_data["email"]
    client_name = assistance_token_data["name"]

    if not openai_api_key:
        assert use_client_openai_api_key is False
        assert client_email is not None
        assert client_name is not None

        openai_api_key = OPENAI_API_KEY

    if client_name is None:
        client_name = data.client_name

    if client_email is None:
        client_email = data.client_email

    record_grouping = urlparse(origin_url).netloc

    agent_message = await run_conversation(
        record_grouping=record_grouping,
        openai_api_key=openai_api_key,
        task_prompt=data.task_prompt,
        agent_name=data.agent_name,
        client_email=client_email,
        client_name=client_name,
        transcript=data.transcript,
    )

    # TODO: Consider having the AI by default check for previous
    # conversations and include a summary of previous conversations
    # within the prompt.
    return ChatResponse(agent_message=agent_message, assistance_token=assistance_token)


async def _verify_and_get_assistance_token_with_data(
    google_id_token: str | None,
    assistance_token: str | None,
    use_client_openai_api_key: bool,
):
    if assistance_token:
        try:
            return _get_assistance_token_data_with_refresh(assistance_token)
        except ExpiredSignatureError:
            pass
        except JWTError as e:
            raise CredentialsException from e

    if google_id_token:
        return await _create_assistance_token_from_google_id(
            google_id_token, use_client_openai_api_key=use_client_openai_api_key
        )

    if not use_client_openai_api_key:
        raise CredentialsException

    return _create_anonymous_client_side_key_token()


def _create_anonymous_client_side_key_token():
    initial_assistance_token_data = {
        "email": None,
        "name": None,
        "use_client_openai_api_key": True,
    }

    return _create_assistance_token(initial_data=initial_assistance_token_data)


class AssistanceTokenData(TypedDict):
    email: str | None
    name: str | None
    use_client_openai_api_key: bool
    exp: datetime


class AssistanceTokenResponses(NamedTuple):
    assistance_token: str
    assistance_token_data: AssistanceTokenData


def _get_assistance_token_data_with_refresh(assistance_token: str):
    payload = jwt.decode(assistance_token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

    assistance_token_data = AssistanceTokenData(
        email=payload["email"],
        name=payload["name"],
        use_client_openai_api_key=payload["use_client_openai_api_key"],
        exp=datetime.utcfromtimestamp(payload["exp"]),
    )
    time_left: timedelta = assistance_token_data["exp"] - datetime.utcnow()

    if time_left > ASSISTANCE_TOKEN_REFRESH:
        return AssistanceTokenResponses(assistance_token, assistance_token_data)

    return _create_assistance_token(assistance_token_data)


class GoogleIdTokenData(TypedDict):
    email: str
    given_name: str


async def _create_assistance_token_from_google_id(
    google_id_token: str, use_client_openai_api_key: bool
):
    loop = asyncio.get_event_loop()

    def _sync_task() -> GoogleIdTokenData:
        return id_token.verify_oauth2_token(
            google_id_token, requests.Request(), GOOGLE_OAUTH_CLIENT_ID
        )

    try:
        id_info = await loop.run_in_executor(None, _sync_task)

    except [exceptions.GoogleAuthError, ValueError] as e:
        raise CredentialsException from e

    client_email = id_info["email"]
    client_name = id_info["given_name"]

    initial_assistance_token_data = {
        "email": client_email,
        "name": client_name,
        "use_client_openai_api_key": use_client_openai_api_key,
    }

    return _create_assistance_token(initial_data=initial_assistance_token_data)


def _create_assistance_token(initial_data: dict):
    assistance_token_data: AssistanceTokenData = {
        **initial_data,
        "exp": datetime.utcnow() + ASSISTANCE_TOKEN_EXPIRES,
    }

    assistance_token = jwt.encode(
        assistance_token_data, JWT_SECRET_KEY, algorithm=ALGORITHM
    )

    return AssistanceTokenResponses(assistance_token, assistance_token_data)
