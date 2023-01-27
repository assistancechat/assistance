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

from assistance._agents.conversations import run_student_chat
from assistance._api.login import User


class StudentChatData(BaseModel):
    agent_name: str
    client_name: str
    transcript: str


async def student_chat_start(data: StudentChatData, current_user: User):
    response = await run_student_chat(
        agent_name=data.agent_name,
        username=current_user.username,
        client_name=data.client_name,
        transcript=data.transcript,
    )

    return {"response": response}
