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

import asyncio
import logging

import openai

from assistance.store.transcript import store_prompt_transcript

from .cache import message_history


async def run_career_chat_start(
    username: str, client_name: str, agent_name: str, prompt: str
):
    message_history[username] = f"{prompt}\n\n{agent_name}:"

    message = await _run_gpt(username=username, client_name=client_name)

    return message


async def run_career_chat_response(
    username: str, client_name: str, agent_name: str, client_text: str | None
):
    message_history[username] += f"\n\n{client_name}: {client_text}\n\n{agent_name}:"

    message = await _run_gpt(username=username, client_name=client_name)

    return message


async def _run_gpt(username: str, client_name: str):
    model_kwargs = {
        "engine": "text-davinci-003",
        "max_tokens": 256,
        "best_of": 1,
        "stop": f"{client_name}:",
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1,
    }

    message = await call_gpt_and_store_as_transcript(
        record_grouping="career.assistance.chat",
        username=username,
        model_kwargs=model_kwargs,
        prompt=message_history[username],
    )
    message = message.strip()

    message_history[username] += f" {message}"
    logging.info(message_history[username])

    return message


async def call_gpt_and_store_as_transcript(
    record_grouping: str,
    username: str,
    model_kwargs: dict,
    prompt: str,
):
    completions = await openai.Completion.acreate(prompt=prompt, **model_kwargs)
    response: str = completions.choices[0].text

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
