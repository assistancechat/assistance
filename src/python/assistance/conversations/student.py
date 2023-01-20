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
import textwrap

import openai

from assistance.query.from_transcript import query_from_transcript
from assistance.search.search import alphacrucis_search
from assistance.store.transcript import store_prompt_transcript

from .cache import message_history

AGENT_NAME = "Michael"
MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 2,
    # "stop": "{client_name}:",
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}

PROMPT = textwrap.dedent(
    """
        The following transcript is from an ongoing conversation between
        you ({agent_name}) from Assistance.Chat student support services
        and a prospective Alphacrusis student ({client_name}).

        Provide your next response taking into account the
        provided additional information. If the additional information
        is insufficient to respond with confidence make sure to convey
        in your response that you are uncertain/unsure of the accuracy
        of what you are saying.

        Aditional Information:
        {additional_information}

        Transcript:
        {transcript}

        Next Response:
        {agent_name}:
    """
).strip()


async def run_student_chat_start(username: str, client_name: str):
    additional_information = (
        "No aditional information needed as the conversation has not yet begun."
    )
    transcript = "Conversation has not yet begun"

    prompt = PROMPT.format(
        agent_name=AGENT_NAME,
        client_name=client_name,
        additional_information=additional_information,
        transcript=transcript,
    )

    record_grouping = "student.assistance.chat"

    response = await call_gpt_and_store_as_transcript(
        record_grouping=record_grouping,
        username=username,
        model_kwargs=MODEL_KWARGS,
        prompt=prompt,
    )

    message_history[username] += f"{AGENT_NAME}: {response}"

    return response


async def run_student_chat_response(
    username: str, client_name: str, client_text: str | None
):
    transcript = message_history[username] + f"\n\n{client_name}: {client_text}"
    record_grouping = "student.assistance.chat"

    query = await query_from_transcript(
        record_grouping=record_grouping, username=username, transcript=transcript
    )

    additional_information = await alphacrucis_search(
        record_grouping=record_grouping, username=username, query=query
    )

    prompt = PROMPT.format(
        agent_name=AGENT_NAME,
        client_name=client_name,
        additional_information=additional_information,
        transcript=transcript,
    )

    response = await call_gpt_and_store_as_transcript(
        record_grouping=record_grouping,
        username=username,
        model_kwargs=MODEL_KWARGS,
        prompt=prompt,
    )

    message_history[username] = transcript + f"\n\n{AGENT_NAME}: {response}"

    return response


async def call_gpt_and_store_as_transcript(
    record_grouping: str,
    username: str,
    model_kwargs: dict,
    prompt: str,
):
    completions = await openai.Completion.acreate(prompt=prompt, **model_kwargs)
    response: str = completions.choices[0].text.strip()

    asyncio.create_task(
        store_prompt_transcript(
            record_grouping=record_grouping,
            username=username,
            model_kwargs=model_kwargs,
            prompt=prompt,
            response=response,
        )
    )

    return response
