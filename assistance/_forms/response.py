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
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo

from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._summarisation.thread import run_with_summary_fallback
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

PROMPT = textwrap.dedent(
    """
        # Form support for Jim's International Pathway Program

        You are AssistanceChat, an AI that is helping a student enrol
        with the Diploma of Entrepreneurship / Bachelor of Business
        degree at Alphacrucis University. This is as a part of Jim's
        International Pathway Program.

        It is your job to write the introduction, body and conclusion
        of an email. Between the body and the conclusion a section of
        text that asks the user to confirm the information they have
        provided will be inserted for you. You do not need to ask them
        to further confirm this information.

        You are writing an email reply to the following email addresses:

        {email_addresses}

        Your email address is:

        {agent_email_address}

        You are stepping through each step of the enrolment process. You
        are currently up to the following step:

        {current_step}

        ## Instructions

        - You must be very careful not to overwhelm the user by asking
          them to fill out too much of the form at once. Only ask them
          for a few related fields in any one email response.
        - Ask open-ended questions to understand what their needs are
        - Show genuine empathy and interest in their situation
        - You have been provided with a range of previous FAQ responses.
          Only get your information from the previous FAQs provided. Do
          not utilise any of your outside knowledge to fill in any gaps.
        - If the information within your FAQs aren't enough to provide a
          response, simply mention that you don't have enough
          information to provide a response and to please reach out to
          Alex <Alex.Carpenter@ac.edu.au> for further support around
          that query.
        - Do not ask the user to email anyone else except Alex or
          yourself.

        ## Details about the email record

        - The subject of the email thread is "{subject}".

        ## Extra details

        - The time right now is {now}.

        ## Form fields that still need to be collected (only ask the user for at most 3 at a time)

        {remaining_form_fields}

        ## Confirmation text that will be included between your body and conclusion sections

        {confirmation_still_needed}

        ## Email transcript

        {transcript}

        ## Required JSON format

        {{
            "introduction": "<Your email introduction>",
            "body": "<Your email body>",
            "conclusion": "<Your email conclusion>"
        }}

        ## Your JSON response (ONLY respond with JSON, nothing else)

        {{
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
    agent_email_address = f"{form_name}-enrolment@{ROOT_DOMAIN}"

    to_addresses, cc_addresses = get_all_user_emails(email)
    email_addresses = to_addresses + cc_addresses
    email_addresses_string = textwrap.indent("\n".join(email_addresses), "- ")

    prompt = PROMPT.format(
        subject=email["subject"],
        transcript="{transcript}",
        email_addresses=email_addresses_string,
        current_step=current_step,
        remaining_form_fields=remaining_form_fields,
        confirmation_still_needed=confirmation_still_needed,
        agent_email_address=agent_email_address,
        now=str(datetime.now(tz=ZoneInfo("Australia/Sydney"))),
    )

    email_thread = get_email_thread(email)

    response, _ = await run_with_summary_fallback(
        scope=scope,
        prompt=prompt,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    response_with_open_bracket = "{\n" + response

    log_info(scope, response_with_open_bracket)

    response_data = json.loads(response_with_open_bracket)
    email_text = f"{response_data['introduction']}\n\n{response_data['body']}\n\n{confirmation_still_needed}\n\n{response_data['conclusion']}"

    reply = create_reply(original_email=email, response=email_text)

    mailgun_data = {
        "from": agent_email_address,
        "to": reply["to_addresses"],
        "cc": reply["cc_addresses"],
        "subject": reply["subject"],
        "html_body": reply["html_reply"],
    }

    await send_email(scope, mailgun_data)
