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

from assistance._config import DEFAULT_OPENAI_MODEL

from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key
from assistance._logging import log_info

from assistance._summarisation.thread import run_with_summary_fallback
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
        # Overview

        You have been provided with an email transcript.

        You are undergoing the process of filling out a form on the
        behalf of the user.

        Your current task is to determine whether or not the user is
        ready to be asked more questions to fill out the form. If they
        haven't yet responded to your previous queries, or they have
        questions of their own, this is a good indicator that they are
        not yet ready to continue with the form.

        ## The email transcript

        {transcript}

        ## Example required JSON format

        {
            "thinking-step-by-step": "<thought process for your decision>"
            "is-the-user-ready-to-continue": <true or false>,
            "justification": "<the justification for your choice goes here>"
        }

        ## Your JSON response
    """
).strip()


async def check_if_user_is_ready_to_continue(email: Email) -> bool:
    scope = email["user_email"]

    email_thread = get_email_thread(email)

    response = await run_with_summary_fallback(
        scope=scope,
        prompt=PROMPT,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    is_the_user_ready_to_continue = json.loads(response)[
        "is-the-user-ready-to-continue"
    ]

    return is_the_user_ready_to_continue
