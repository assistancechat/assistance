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
from assistance._completions import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._types import Email

from .discourse_summary import run_with_summary_fallback
from .executive_function_system import get_tools_and_responses

OPEN_AI_API_KEY = get_openai_api_key()
SERP_API_KEY = get_serp_api_key()

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 2,
    "presence_penalty": 2,
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

        You are an AI Assistant helping a student enrol with the
        Diploma of Entrepreneurship / Bachelor of Business degree at
        Alphacrucis University.

        You are stepping through each step of the enrolment process. You
        are currently up to the following step:

        - Requesting the user for a scan or picture of their passport.

        ## Instructions

        - Ask open-ended questions to understand what their needs are
        - Show genuine empathy and interest in their situation
        - You have been provided with a range of tool results. Only get
          your information from the tool results provided. Do not
          utilise any of your outside knowledge to fill in any gaps.
        - If the information within your tools isn't enough to provide
          a response, simply mention that you don't have enough
          information to provide a response and to please reach out to
          me@simonbiggs.net for further support around that query.

        ## Details about the email record

        - The subject of the email thread is "{subject}".

        ## Extra details

        - The time right now is {now}.

        ## Email transcript

        {transcript}
    """
).strip()


async def react_to_enrolment_request(email: Email):
    scope = email["user_email"]

    email_thread, prompt = await _get_prompt(email)

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
        "from": f"enrolment@{ROOT_DOMAIN}",
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


async def _get_prompt(email: Email):
    scope = email["user_email"]

    parser = EmailReplyParser()
    email_message = parser.read(email["plain_all_content"])
    replies = [str(item) for item in email_message.replies[-1::-1]]

    replies[-1] = f"On {email['date']}, {email['from']} wrote:\n{replies[-1]}"

    log_info(scope, json.dumps(replies, indent=2))

    task = TASK.format(
        subject=email["subject"],
        transcript="{transcript}",
        now=str(datetime.now(tz=ZoneInfo("Australia/Sydney"))),
    )

    tools = await get_tools_and_responses(
        scope=scope,
        task=task,
        email_thread=replies,
        example_tool_use=EXAMPLE_TOOL_USE,
        extra_tools=EXTRA_TOOLS,
    )
    keys_to_keep = ["tool", "result"]

    filtered_tools = []
    for tool in tools:
        filtered_tool = {key: tool[key] for key in keys_to_keep}
        filtered_tools.append(filtered_tool)

    tools_string = json.dumps(filtered_tools, indent=2)

    prompt = EMAIL_PROMPT.format(
        task=task, tool_results=tools_string, transcript="{transcript}"
    )

    return replies, prompt
