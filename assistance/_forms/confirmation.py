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

from assistance._config import DEFAULT_OPENAI_MODEL, FormItem

from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key
from assistance._logging import log_info

from assistance._summarisation.thread import run_with_summary_fallback
from assistance._types import Email

OPEN_AI_API_KEY = get_openai_api_key()

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


TASK = textwrap.dedent(
    """
        # Overview

        You have been provided with an email transcript as well as a
        range of form fields that you have extracted from previous email
        records.

        Once a form field item has been extracted the user is asked to
        confirm whether or not the extracted value is correct. It is
        your task to identify for the following form fields whether or
        not the extracted value has been explicitly confirmed by the
        user within the email record.

        DO NOT include a field in your response at all if it has not
        been able to be determined. DO NOT use null or N/A as a value,
        instead, just do not include that field in your response.

        For every field that you do include YOU MUST include both the
        "value" and the "confirmed" fields.

        ## Descriptions of the form fields that need to be confirmed

        {confirmation_form_fields_text}

        ## The email transcript

        {transcript}

        ## Example required JSON format

        {{
            "personal.passport-number": {{
                "value": "<passport number goes here>",
                "confirmed": <true or false>
            }},
            "contact.email": {{
                "value": "<email goes here>",
                "confirmed": <true or false>
            }}
        }}
        {error_details}
        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def confirming_form_items(
    email: Email, confirmation_form_fields_text: str, error: str | None
) -> dict[str, FormItem]:
    scope = email["user_email"]

    email_thread = get_email_thread(email)

    if error is not None:
        error_details = textwrap.dedent(
            f"""
                ## Your previous attempt gave the following error message

                {error}
            """
        ).strip()
    else:
        error_details = ""

    prompt = TASK.format(
        transcript="{transcript}",
        confirmation_form_fields_text=confirmation_form_fields_text,
        error_details=error_details,
    )

    response = await run_with_summary_fallback(
        scope=scope,
        prompt=prompt,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    confirmation_record = json.loads(response)

    return confirmation_record
