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
import re
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo

from mailparser_reply import EmailReplyParser

from assistance import _ctx
from assistance._openai import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._summarisation.thread import run_with_summary_fallback
from assistance._tooling.executive_function_system import get_tools_and_responses
from assistance._types import Email

OPEN_AI_API_KEY = get_openai_api_key()
SERP_API_KEY = get_serp_api_key()

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


EMAIL_PROMPT = textwrap.dedent(
    """
        {task}

        ## Tool results

        {tool_results}

        ## Your email response (email content ONLY)
    """
).strip()


TASK = textwrap.dedent(
    """
        ## Overview

        You are an AI Assistant named Meshach helping a student enrol
        with the Diploma of Entrepreneurship / Bachelor of Business
        degree at Alphacrucis University. You are about to write a reply
        to the following email addresses:

        {email_addresses}

        You are stepping through each step of the enrolment process. You
        are currently up to the following step:

        {current_step}

        ## Instructions

        - You must be very careful not to overwhelm the user by asking
          them to fill out too much of the form at once. Only ask them
          for a few related fields in any one email response.
        - Ask open-ended questions to understand what their needs are
        - Show genuine empathy and interest in their situation
        - You have been provided with a range of tool results. Only get
          your information from the tool results provided. Do not
          utilise any of your outside knowledge to fill in any gaps.
        - If the information within your tools isn't enough to provide
          a response, simply mention that you don't have enough
          information to provide a response and to please reach out to
          simon@assistance.chat for further support around that query.
        - Do not ask the user to email anyone else except those at the
          assistance.chat domain.
        - If you have some results that need to be confirmed, make sure
          to ask the user to confirm a few of them in your response.

        ## Details about the email record

        - The subject of the email thread is "{subject}".

        ## Extra details

        - The time right now is {now}.

        ## Form fields that still need to be collected (only ask a few at once)

        {remaining_form_fields}

        ## Form items that have been collected from the user and need user confirmation

        {confirmation_still_needed}

        ## Email transcript

        {transcript}
    """
).strip()


async def write_and_send_email_response(
    email: Email,
    form_name: str,
    current_step: str,
    remaining_form_fields: str,
    confirmation_still_needed: str,
):
    scope = email["user_email"]

    to_addresses, cc_addresses = get_all_user_emails(email)
    email_addresses = to_addresses + cc_addresses
    email_addresses_string = textwrap.indent("\n".join(email_addresses), "- ")

    task = TASK.format(
        subject=email["subject"],
        transcript="{transcript}",
        email_addresses=email_addresses_string,
        current_step=current_step,
        remaining_form_fields=remaining_form_fields,
        confirmation_still_needed=confirmation_still_needed,
        now=str(datetime.now(tz=ZoneInfo("Australia/Sydney"))),
    )

    email_thread, prompt = await _get_prompt(email, task)

    response = await run_with_summary_fallback(
        scope=scope,
        prompt=prompt,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    reply = create_reply(original_email=email, response=response)

    mailgun_data = {
        "from": f"{form_name}-enrolment@{ROOT_DOMAIN}",
        "to": reply["to_addresses"],
        "cc": reply["cc_addresses"],
        "subject": reply["subject"],
        "html_body": reply["html_reply"],
    }

    await send_email(scope, mailgun_data)


EXAMPLE_TOOL_USE = textwrap.dedent(
    """
        [
            {{
                "id": 0,
                "step_by_step_thought_process": "I will start by using the 'now' tool to get the current date and time.",
                "tool": "now",
                "args": [],
                "score": 9,
                "confidence": 8
            }},
            {{
                "id": 1,
                "step_by_step_thought_process": "I am going to search for more details about the courses at Alphacrucis.",
                "tool": "internet_search",
                "args": ["Courses at Alphacrucis University"],
                "score": 9,
                "confidence": 8
            }}
        ]
    """
).strip()


EXTRA_TOOLS = ""


async def _get_prompt(email: Email, task: str):
    scope = email["user_email"]

    email_thread = get_email_thread(email)

    log_info(scope, json.dumps(email_thread, indent=2))

    tools = await get_tools_and_responses(
        scope=scope,
        task=task,
        email_thread=email_thread,
        example_tool_use=EXAMPLE_TOOL_USE,
        extra_tools=EXTRA_TOOLS,
    )
    keys_to_keep = ["step_by_step_thought_process", "tool", "args", "result"]

    filtered_tools = []
    for tool in tools:
        filtered_tool = {key: tool[key] for key in keys_to_keep}
        filtered_tools.append(filtered_tool)

    tools_string = json.dumps(filtered_tools, indent=2)

    prompt = EMAIL_PROMPT.format(
        task=task, tool_results=tools_string, transcript="{transcript}"
    )

    return email_thread, prompt
