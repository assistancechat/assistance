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


from fastapi import APIRouter, Depends
from pydantic import BaseModel

from assistance.api.login import User, get_current_user
from assistance.conversations import run_career_chat_response, run_career_chat_start


class ChatStartData(BaseModel):
    client_name: str
    agent_name: str
    prompt: str


router = APIRouter(
    prefix="/chat",
    responses={404: {"description": "Not found"}},
)


@router.post("/career/start")
@router.post("/start")
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


@router.post("/career/start")
@router.post("/continue")
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
