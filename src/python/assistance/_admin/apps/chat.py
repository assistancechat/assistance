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


import streamlit as st

from assistance._admin import categories
from assistance._api.login import User
from assistance._api.raw import chat

CATEGORY = categories.DEMO
TITLE = "Student Assistance Chat"


MOCK_USER = User(username="MockUsername")
AGENT_NAME = "Michael"


async def main():
    client_name = st.text_input("Your name")

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    transcript = _create_transcript(
        agent_name=AGENT_NAME,
        client_name=client_name,
        conversation=st.session_state.conversation,
    )

    st.write(transcript)

    if len(st.session_state.conversation) % 2 == 0:
        data = chat.StudentChatData(
            agent_name=AGENT_NAME,
            client_name=client_name,
            transcript=transcript,
        )

        api_result = await chat.student_chat(data=data, current_user=MOCK_USER)
        response = api_result["response"]

        st.session_state.conversation.append(response)
        st.experimental_rerun()

    else:
        user_input = st.text_input()
        st.button("Submit")

        st.session_state.conversation.append(user_input)
        st.experimental_rerun()


def _create_transcript(
    agent_name: str, client_name: str, conversation: list[str]
) -> str:
    transcript_as_list = []

    for i, item in enumerate(conversation):
        if i % 2 == 0:
            transcript_as_list.append(f"{agent_name}: {item}")
        else:
            transcript_as_list.append(f"{client_name}: {item}")

    transcript = "\n\n".join(transcript_as_list)

    return transcript
