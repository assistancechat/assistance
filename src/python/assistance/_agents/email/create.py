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

import json
import logging
import re
import textwrap

import aiofiles
import openai

from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key
from assistance._mailgun import send_email
from assistance._paths import PROMPTS as PROMPTS_PATH

from .reply import create_reply
from .types import Email

OPEN_AI_API_KEY = get_openai_api_key()


JSON_SECTION = "1. JSON details (MUST be valid JSON):"
TOOL_RESULT_SECTION = "2. Tool result:"
RESPONSE_SECTION = "3. Next email to send to user:"

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 1,
    "stop": [TOOL_RESULT_SECTION, "[END]"],
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}


PROMPT = textwrap.dedent(
    """
        You are the Create Assistant and you are sending and receiving
        multiple emails from "{from_string}".

        The record of these emails is at the end of this document
        between the tags [EMAIL BODY START] and [END].

        Using their email sent to you determine an appropriate `prompt`
        and an appropriate `agent_name`.

        They do not have to explicitly declare the `agent_name` or the
        `prompt` but you must be able to create a reasonable
        `agent_name` and `prompt` from the email.

        Once the agent has been created it will respond to the user
        automatically when they email {{agent_name}}@{domain}.
        `agent_name` must be able to be prepended to @{domain} in order
        to create a valid email address.

        [YOUR TRAITS START]

            - You personalise with the user's name
            - You show genuine empathy and interest in the user's
              situation

        [END]

        [RESPONSE OVERVIEW START]

            Within your response you are required to provide three
            sections of information:

            - The first is the JSON details that will be used to create
              the agent.
            - The second is the result of the agent creation tool after
              you have called the tool.
            - The third is the response that will be sent to the user
              either to confirm that the agent has been created or to
              inform them that the agent could not be created just yet
              with the current information and provide the user with the
              reason why.

        [END]

        [VALID PROMPTS START]

            Prompts are only valid if they are able to be used to create
            a valid agent within the agent restrictions.

        [END]

        [AGENT CREATION REQUIREMENTS START]

            - Only begin to create the agent if you are absolutely sure
              that that is what the user wants (confirm with them
              first).
            - Only begin to create the agent if the user has provided a
              valid `agent_name`.
            - Only begin to create the agent if the user has provided a
              valid `prompt`.

        [END]

        [TASKS ON AGENT CREATION START]

            - Once you have successfully created the agent make sure to
              provide instructions within your email response on how to
              use the agent that has now been created for them.
            - Only provide this information once the agent has been
              successfully created.

        [END]

        [RESPONSE FORMAT START]

            {JSON_SECTION}

            {{
                "ready_to_create_agent": [true or false],
                "agent_name": "<Agent name goes here>",
                "prompt": "<Prompt goes here, include new lines as \\n>"
            }}

            {TOOL_RESULT_SECTION}

            [Result of agent creation tool goes here]

            {RESPONSE_SECTION}

            [Response to user goes here]

        [END]

        [EMAIL SUBJECT START]

            {subject}

        [END]

        [EMAIL BODY START]

        {body_plain}

        [END]

        Go!

        {JSON_SECTION}
    """
).strip()


async def create_agent(email: Email):
    prompt = PROMPT.format(
        domain=ROOT_DOMAIN,
        body_plain=textwrap.indent(email["body-plain"], "    "),
        from_string=email["from"],
        user_email_address=email["user-email"],
        subject=email["subject"],
        JSON_SECTION=JSON_SECTION,
        TOOL_RESULT_SECTION=TOOL_RESULT_SECTION,
        RESPONSE_SECTION=RESPONSE_SECTION,
    )
    logging.info(prompt)

    for _ in range(3):
        completions = await openai.Completion.acreate(
            prompt=prompt, api_key=OPEN_AI_API_KEY, **MODEL_KWARGS
        )
        response: str = completions.choices[0].text.strip()

        try:
            json_data = json.loads(response)
            break
        except json.JSONDecodeError:
            json_data = {}

    logging.info(response)

    tool_response: str | None = None

    try:
        if json_data["ready_to_create_agent"]:
            agent_name: str = json_data["agent_name"]
            agent_name = agent_name.lower().replace(" ", "-")

            agent_email = f"{agent_name}@{ROOT_DOMAIN}".lower()
            match = re.search(
                r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$",
                agent_email,
            )
            if match is None:
                raise ValueError(
                    f"Invalid agent_name: {agent_name}. The created email "
                    f"address of {agent_email} is not a valid address."
                )

            json_data["agent_name"] = agent_name

            from .default import DEFAULT_TASKS

            if agent_name in DEFAULT_TASKS.keys():
                raise ValueError(
                    "Cannot create an agent with a reserved name. "
                    f"{agent_name} is a reserved name."
                )

            tool_response = await _create_email_agent(
                email["user-email"], agent_name, json_data["prompt"]
            )
        else:
            tool_response = "Agent not created `ready_to_create_agent` was set to false"

    except Exception as e:
        tool_response = f"Agent not created due to error: {e}"

    assert tool_response is not None

    prompt += (
        "\n\n"
        + json.dumps(json_data, indent=2)
        + "\n\n"
        + TOOL_RESULT_SECTION
        + "\n\n"
        + tool_response
        + "\n\n"
        + RESPONSE_SECTION
    )

    logging.info(prompt)

    completions = await openai.Completion.acreate(
        prompt=prompt, api_key=OPEN_AI_API_KEY, **MODEL_KWARGS
    )
    response: str = completions.choices[0].text.strip()

    subject, total_reply = create_reply(
        subject=email["subject"],
        body_plain=email["body-plain"],
        response=response,
        from_string=email["from"],
    )

    mailgun_data = {
        "from": f"{email['agent-name']}@{ROOT_DOMAIN}",
        "to": email["user-email"],
        "subject": subject,
        "text": total_reply,
    }

    await send_email(mailgun_data)


async def _create_email_agent(user_email_address: str, agent_name: str, prompt: str):
    path_to_new_prompt = PROMPTS_PATH / user_email_address / agent_name
    path_to_new_prompt.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(path_to_new_prompt, "w") as f:
        await f.write(prompt)

    return "Email agent successfully created"
