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

import logging

from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel

from assistance._agents.conversations import run_conversation
from assistance._config import get_google_oauth_client_id

CLIENT_ID = get_google_oauth_client_id()


class StudentChatData(BaseModel):
    token: str
    agent_name: str
    task_prompt: str
    transcript: str | None = None


async def run_chat(data: StudentChatData):
    # TODO: Make this run with asyncio instead
    # TODO: Separate out the login into its own API request and create
    # our own JWT that doesn't need to talk to Google servers every time
    # TODO: When logging in, able to provide an initial summary of
    # previous conversations back with the API as a greeting message.
    id_info = id_token.verify_oauth2_token(data.token, requests.Request(), CLIENT_ID)
    client_email = id_info["email"]
    client_name = id_info["given_name"]

    logging.info(id_info)

    response = await run_conversation(
        task_prompt=data.task_prompt,
        agent_name=data.agent_name,
        client_email=client_email,
        client_name=client_name,
        transcript=data.transcript,
    )

    return {"response": response}
