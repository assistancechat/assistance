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

import textwrap

from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply
from assistance._keys import get_openai_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._openai import get_completion_only
from assistance._types import Email

OPEN_AI_API_KEY = get_openai_api_key()


MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


PROMPT = textwrap.dedent(
    """
        You are sending and receiving multiple emails from
        "{user_email}". Your email address is {agent_name}@{ROOT_DOMAIN}.

        Task
        ----

        {prompt_task}

        Email subject
        -------------

        {subject}

        The email chain thus far, most recent email first
        -------------------------------------------------

        {body_plain}

        Next email to send to {user_email}
        -----------------------------------
    """
).strip()


async def react_to_custom_agent_request(email: Email, prompt_task: str):
    scope = email["user_email"]

    prompt = PROMPT.format(
        body_plain=email["plain_all_content"],
        user_email=email["user_email"],
        prompt_task=prompt_task,
        agent_name=email["agent_name"],
        subject=email["subject"],
        ROOT_DOMAIN=ROOT_DOMAIN,
    )
    log_info(scope, prompt)

    response = await get_completion_only(
        scope=email["user_email"],
        prompt=prompt,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    reply = create_reply(
        original_email=email,
        response=response,
    )

    mailgun_data = {
        "from": f"{email['agent_name']}@{ROOT_DOMAIN}",
        "to": reply["to_addresses"],
        "cc": reply["cc_addresses"],
        "subject": reply["subject"],
        "plain_body": reply["total_reply"],
    }

    await send_email(scope, mailgun_data)
