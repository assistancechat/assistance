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

import asyncio
import json
import textwrap

from assistance._config import DEFAULT_OPENAI_MODEL
from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key
from assistance._logging import log_info
from assistance._summarisation.thread import run_with_summary_fallback
from assistance._types import Email
from assistance._utilities import items_to_list_string

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
        range of form fields that need to be filled out from the email
        record.

        Determine which fields are able to be accurately extracted and
        present them in JSON format.

        ## Descriptions for each of the form fields

        {form_field_descriptions}

        ## Example required JSON format

        {{
            "an.example.field.item": {{
                "the description of this form item": "<the relevant field description provided above>",
                "section of email transcript": "<section of email transcript that contains this result, leave blank if the not in transcript>",
                "value": "<field result goes here>",
                "does this value match what was within the current email transcript?": <true or false>,
                "could have this response be referred to something else that is not relevant to this field item?": <true or false>
            }},
            "another.example.field.item": {{
                "the description of this form item": "<the relevant field description provided above>",
                "section of email transcript": "<section of email transcript that contains this result, leave blank if the not in transcript>",
                "value": "<field result goes here>",
                "does this value match what was within the current email transcript?": <true or false>,
                "could have this response be referred to something else that is not relevant to this field item?": <true or false>
            }},
            ...
            "last.field.result.that.you.found": {{
                "the description of this form item": "<the relevant field description provided above>",
                "section of email transcript": "<section of email transcript that contains this result, leave blank if the not in transcript>",
                "value": "<field result goes here>",
                "does this value match what was within the current email transcript?": <true or false>,
                "could have this response be referred to something else that is not relevant to this field item?": <true or false>
            }}
        }}

        ## The email transcript

        {transcript}

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def collect_form_items(
    email: Email, split_remaining_form_fields: list[str]
) -> dict[str, str]:
    scope = email["user_email"]

    email_thread = get_email_thread(email)

    coroutines = []

    for form_fields in split_remaining_form_fields:
        coroutines.append(
            _collect_subset_of_form_fields(scope, email_thread, form_fields)
        )

    collected_fields = await asyncio.gather(*coroutines)

    all_collected_fields = {}
    for collected_field in collected_fields:
        all_collected_fields.update(collected_field)

    return all_collected_fields


async def _collect_subset_of_form_fields(
    scope, email_thread, remaining_form_fields_text: str
):
    lines = remaining_form_fields_text.splitlines()

    header_items = items_to_list_string(
        [line.replace("#", "").strip() for line in lines if line.startswith("#")]
    )

    header_text = f"The form items below are only referring to information that is under the following headings:\n{header_items}\n\n"

    updated_lines = [line for line in lines if not line.startswith("#")]

    updated_remaining_form_fields_text = header_text + "\n".join(updated_lines)

    prompt = TASK.format(
        transcript="{transcript}",
        form_field_descriptions=updated_remaining_form_fields_text,
    )

    response, transcript = await run_with_summary_fallback(
        scope=scope,
        prompt=prompt,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    new_form_items = json.loads(response)

    valid_form_items = {}
    for key, item in new_form_items.items():
        value = item["value"]

        if not value:
            continue

        validation = (
            item["section of email transcript"] in transcript
            and value in item["section of email transcript"]
            and item[
                "does this value match what was within the current email transcript?"
            ]
            and not item[
                "could have this response be referred to something else that is not relevant to this field item?"
            ]
        )

        if validation:
            valid_form_items[key] = value

    return valid_form_items
