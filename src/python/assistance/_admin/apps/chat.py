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

    if not client_name:
        st.stop()

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    if len(st.session_state.conversation) % 2 == 0:
        transcript = _create_transcript(
            agent_name=AGENT_NAME,
            client_name=client_name,
            conversation=st.session_state.conversation,
        )

        data = chat.ChatData(
            agent_name=AGENT_NAME,
            client_name=client_name,
            transcript=transcript,
        )

        api_result = await chat.run_chat(data=data, current_user=MOCK_USER)
        response = api_result["response"]

        st.session_state.conversation.append(response)

    transcript = _create_transcript(
        agent_name=AGENT_NAME,
        client_name=client_name,
        conversation=st.session_state.conversation,
    )

    with st.form("conversation-form"):
        st.write(transcript)

        st.text_input("Enter your message", key="user_input")

        cols = st.columns([1, 1])

        with cols[0]:
            st.form_submit_button("Send message", on_click=_submit)

        with cols[1]:
            st.form_submit_button("Reset Chat", on_click=_reset)


def _submit():
    st.session_state.conversation.append(st.session_state["user_input"])
    st.session_state["user_input"] = ""


def _reset():
    st.session_state.conversation = []
    st.session_state["user_input"] = ""


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
