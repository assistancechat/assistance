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

import logging
import re
import aiofiles
import textwrap

import openai

from assistance._paths import PROMPTS as PROMPTS_PATH
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key
from assistance._mailgun import send_email

OPEN_AI_API_KEY = get_openai_api_key()


MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 1,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}


PROMPT = textwrap.dedent(
    """
        You are sending and receiving multiple emails from
        "{from_string}". Your email address is {agent_name}@{ROOT_DOMAIN}.

        Task
        ----

        {prompt_task}

        The email chain thus far, most recent email first
        -------------------------------------------------

        {body_plain}

        Next email to send to {from_string}
        -----------------------------------
    """
).strip()


async def react_to_custom_agent_request(
    from_string: str,
    user_email_address: str,
    prompt_task: str,
    subject: str,
    body_plain: str,
    agent_name: str,
):
    prompt = PROMPT.format(
        body_plain=body_plain,
        from_string=from_string,
        prompt_task=prompt_task,
        agent_name=agent_name,
        ROOT_DOMAIN=ROOT_DOMAIN,
    )
    logging.info(prompt)

    completions = await openai.Completion.acreate(
        prompt=prompt, api_key=OPEN_AI_API_KEY, **MODEL_KWARGS
    )
    response: str = completions.choices[0].text.strip()

    logging.info(response)

    if not subject.startswith("Re:"):
        subject = f"Re: {subject}"

    mailgun_data = {
        "from": f"{agent_name}@{ROOT_DOMAIN}",
        "to": user_email_address,
        "subject": subject,
        "text": response,
    }

    await send_email(mailgun_data)
