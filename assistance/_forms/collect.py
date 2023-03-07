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
from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._summarisation.thread import run_with_summary_fallback
from assistance._types import Email

from .build import walk_and_build_remaining_form_fields

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


TASK = textwrap.dedent(
    """
        # Overview

        You have been provided with an email transcript as well as a
        range of form fields that need to be filled out from the email
        record.

        Determine which fields are able to be accurately extracted at
        present them in JSON format. Only provide the fields that you
        are able to extract with confidence.

        ## The email transcript

        {transcript}

        ## Descriptions for each of the form fields

        {form_field_descriptions}

        ## Example required JSON format

        {{
            "personal.passport-number": "<number goes here>",
            "contact.email": "<email goes here>"
        }}

        ## Your JSON response
    """
).strip()


async def collect_form_items(email: Email):
    scope = email["user_email"]

    email_thread = get_email_thread(email)

    # prompt = TASK.format(
    #     transcript="{transcript}",
    #     form_field_descriptions=,

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
