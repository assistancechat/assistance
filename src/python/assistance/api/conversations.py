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

import logging

import openai

from .utilities import LRUCache

# TODO: Make this time expiration based.
message_history = LRUCache(10000)


def run_chat_start(username: str, client_name: str, agent_name: str, prompt: str):
    message_history[username] = f"{prompt}\n\n{agent_name}:"

    message = _run_gpt(username=username, client_name=client_name)

    return message


def run_chat_response(
    username: str, client_name: str, agent_name: str, client_text: str | None
):
    message_history[username] += f"\n\n{client_name}: {client_text}\n\n{agent_name}:"

    message = _run_gpt(username=username, client_name=client_name)

    return message


def _run_gpt(username: str, client_name: str):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message_history[username],
        max_tokens=256,
        best_of=2,
        stop=f"{client_name}:",
        temperature=0.7,
        top_p=1,
        frequency_penalty=0.1,
        presence_penalty=0.1,
    )

    message: str = completions.choices[0].text.strip()
    message_history[username] += f" {message}"

    logging.info(message_history[username])

    return message
