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

from pydantic import BaseModel

from assistance._agents.conversations import (
    run_student_chat_response,
    run_student_chat_start,
)
from assistance._api.login import User


class StudentChatStartData(BaseModel):
    client_name: str


class StudentChatContinueData(BaseModel):
    client_name: str
    client_text: str


async def student_chat_start(data: StudentChatStartData, current_user: User):
    response = await run_student_chat_start(
        username=current_user.username,
        client_name=data.client_name,
    )

    return {"response": response}


async def student_chat_continue(
    data: StudentChatContinueData,
    current_user: User,
):
    response = await run_student_chat_response(
        username=current_user.username,
        client_name=data.client_name,
        client_text=data.client_text,
    )

    return {"response": response}
