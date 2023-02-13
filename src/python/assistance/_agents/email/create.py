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

# Prompt inspired by the work provided under an MIT license over at:
# https://github.com/hwchase17/langchain/blob/ae1b589f60a/langchain/agents/conversational/prompt.py#L1-L36

import json
import asyncio
import logging
import re
import aiofiles
import textwrap
from typing import Callable, Coroutine

from thefuzz import process as fuzz_process

import openai

from assistance._paths import PROMPTS as PROMPTS_PATH
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key

OPEN_AI_API_KEY = get_openai_api_key()


MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 1,
    "stop": "Observation:",
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}


PROMPT = textwrap.dedent(
    """
        A user is emailing you with the aim to create an automated
        emailing agent. To create an emailing agent there needs to be
        a prompt as well as the email agent_name of the agent. They may
        provide the prompt to you, or with your help and their feedback
        you may create a prompt for them.

        Once the user has provided an agent_name the email agent will be
        created to respond to the user automatically when they email
        [agent_name]@{domain}. agent_name must be able to be prepended
        to @{domain} in order to create a valid email address.

        Within your response you are required to provide two sections of
        information. The first is the JSON details that will be used to
        create the agent. Within this first section you also declare
        whether or not the agent is ready to be created. The second is
        the response that will be sent to the user either to confirm
        that the agent or to inform them that the agent could not be
        created and provide the user with the reason why.

        Before being ready to create the agent make sure to confirm with
        the user the prompt and the [agent_name]@{domain} that will be
        created for them.

        Once you are ready to create the agent make sure to provide
        instructions within your email response on how to use the agent
        that will be created.

        Response format
        ---------------

        JSON details:

        {
            "ready_to_create_agent": [True or False],
            "agent_name": [Agent name goes here],
            "prompt": [Prompt goes here],
        }

        Email response:

        [Response to user goes here]

        The email chain thus far, most recent email first
        -------------------------------------------------

        {body_plain}

        Response
        --------
    """
).strip()


async def react_to_create_domain(from_string: str, body_plain: str):
    prompt = PROMPT.format(domain=ROOT_DOMAIN, body_plain=body_plain)
    logging.info(prompt)

    completions = await openai.Completion.acreate(
        prompt=prompt, api_key=OPEN_AI_API_KEY, **MODEL_KWARGS
    )
    response: str = completions.choices[0].text.strip()

    line_by_line = response.splitlines()

    json_details_line = fuzz_process.extractOne("JSON details:", line_by_line)
    email_response_line = fuzz_process.extractOne("Email response:", line_by_line)

    json_details_index = line_by_line.index(json_details_line[0])
    email_response_index = line_by_line.index(email_response_line[0])

    json_details = "\n".join(
        line_by_line[json_details_index + 1 : email_response_index]
    ).strip()
    email_response = "\n".join(line_by_line[email_response_index + 1 :]).strip()

    try:
        json_data = json.loads(json_details)

        if json_data["ready_to_create_agent"]:
            logging.info("Creating email agent")
            await _create_email_agent(
                from_string, json_data["agent_name"], json_data["prompt"]
            )

    except Exception as e:
        logging.info(e)

    return email_response


async def _create_email_agent(from_string: str, agent_name: str, prompt: str):
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", from_string)
    user_email_address = match.group(0)

    path_to_new_prompt = PROMPTS_PATH / user_email_address / agent_name
    path_to_new_prompt.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(path_to_new_prompt, "w") as f:
        await f.write(prompt)
