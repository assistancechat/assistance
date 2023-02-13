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


JSON_SECTION = "1. JSON details (MUST be valid JSON):"
TOOL_RESULT_SECTION = "2. Tool result:"
RESPONSE_SECTION = "3. Next email to send to user:"

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 1,
    "stop": TOOL_RESULT_SECTION,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}


PROMPT = textwrap.dedent(
    """
        You are the Create Assistant and you are sending and receiving
        multiple emails from "{from_string}". It is your goal to create
        an automated mailing assistant for them. This automated agent
        will be a large language model that will not have access to the
        internet or any tooling.

        To create an emailing agent there needs to be a prompt as well
        as an agent_name of the agent to be created. They may provide
        the prompt to you, or with your help and their feedback you may
        create a prompt for them.

        Once the user has provided an `agent_name` the email agent will
        be created to respond to the user automatically when they email
        {{agent_name}}@{domain}. `agent_name` must be able to be
        prepended to @{domain} in order to create a valid email address.

        Only they will be able to use this created agent. And only if
        they use their {user_email_address} email address.

        Keep in mind the below points in everything you say:

        - Personalise with the user's name
        - Ask open-ended questions to understand the user's needs
        - Show genuine empathy and interest in user's situation
        - If they haven't provided a prompt, or you suspect they might
          like help expanding their prompt, give them some ideas and
          examples that can be used to create the agent.

        DO NOT CREATE AN AGENT if the user has not yet provided
        SUFFICIENT information. Instead have an email conversation with
        them, helping them to appropriately create their agent.

        Within your response you are required to provide three sections
        of information:

        - The first is the JSON details that will be used to create the
          agent.
        - The second is the result of the agent creation tool after you
          have called the tool.
        - The third is the response that will be sent to the user either
          to confirm that the agent has been created or to inform them
          that the agent could not be created just yet with the current
          information and provide the user with the reason why.

        Valid prompts
        -------------

        Prompts are only valid if they are able to be used to create a
        valid agent within the agent restrictions.

        Requirements for agent creation
        -------------------------------

        - Only begin to create the agent if you are absolutely sure that
          that is what the user wants (confirm with them first).
        - Only begin to create the agent if the user has provided a
          valid `agent_name`.
        - Only begin to create the agent if the user has provided a
          valid `prompt`.

        Upon successful creation of the agent
        -------------------------------------

        Once you have successfully created the agent make sure to
        provide instructions within your email response on how to use
        the agent that has now been created for them.

        Only provide this information once the agent has been
        successfully created.

        Response format
        ---------------

        {JSON_SECTION}

        {{
            "ready_to_create_agent": [true or false],
            "agent_name": [Agent name goes here],
            "prompt": [Prompt goes here]
        }}

        {TOOL_RESULT_SECTION}

        [Result of agent creation tool goes here]

        {RESPONSE_SECTION}

        [Response to user goes here]

        The email chain thus far, most recent email first
        -------------------------------------------------

        Subject: {subject}

        Email body:
        {body_plain}

        Response
        --------
        {JSON_SECTION}
    """
).strip()


async def react_to_create_domain(from_string: str, subject: str, body_plain: str):
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", from_string)
    user_email_address = match.group(0).lower()

    prompt = PROMPT.format(
        domain=ROOT_DOMAIN,
        body_plain=body_plain,
        from_string=from_string,
        user_email_address=user_email_address,
        subject=subject,
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

        if json_data["ready_to_create_agent"]:
            logging.info("Creating email agent")
            tool_response = await _create_email_agent(
                user_email_address, agent_name, json_data["prompt"]
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

    if not subject.startswith("Re:"):
        subject = f"Re: {subject}"

    mailgun_data = {
        "from": f"create@{ROOT_DOMAIN}",
        "to": user_email_address,
        "subject": subject,
        "text": response,
    }

    await send_email(mailgun_data)


async def _create_email_agent(user_email_address: str, agent_name: str, prompt: str):
    path_to_new_prompt = PROMPTS_PATH / user_email_address / agent_name
    path_to_new_prompt.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(path_to_new_prompt, "w") as f:
        await f.write(prompt)

    return "Email agent successfully created"
