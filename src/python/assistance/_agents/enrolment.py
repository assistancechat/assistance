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

from .discourse_summary import EmailInThread, run_with_summary_fallback
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

        Introduce yourself, respond to any student queries, and request
        the student begins the enrolment process by providing you a scan
        of their passport as an email attachment.

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

        - Emails are organised so that the most recent email in the
          thread is first.
        - Previous emails in the thread are indented with ">".
        - The subject of the email thread is "{subject}".

        ## Extra details

        - The time right now is {now}.

        ## Email record

        On {date}, {from_string} wrote:
        {email_content}
    """
).strip()


async def react_to_enrolment_request(
    user_details: dict,
    email: Email,
):
    scope = email["user_email"]

    prompt = await _prompt_as_email_thread(email)

    response = await get_completion_only(
        scope=scope,
        prompt=prompt,
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


async def _prompt_as_email_thread(email: Email):
    scope = email["user_email"]

    parser = EmailReplyParser()
    email_message = parser.read(email["plain_all_content"])
    replies = [str(item) for item in email_message.replies[-1::-1]]

    log_info(scope, json.dumps(replies, indent=2))

    to_addresses, cc_addresses = get_all_user_emails(email)
    email_addresses = to_addresses + cc_addresses
    email_addresses_string = textwrap.indent("\n".join(email_addresses), "- ")

    reversed_email_thread = filtered_email_content.split("On")

    tools = await get_tools_and_responses(
        scope=scope, task=TASK, email_thread=email_thread
    )
    keys_to_keep = ["tool", "result"]

    prompt = EMAIL_PROMPT.format(
        email_content=filtered_email_content,
        subject=email["subject"],
        date=email["date"],
        from_string=email["from"],
        root_domain=ROOT_DOMAIN,
        email_from=email["from"],
        stripped_text=email["plain_no_replies"],
        email_addresses=email_addresses_string,
        now=str(datetime.now(tz=ZoneInfo("Australia/Sydney"))),
    )

    return prompt
