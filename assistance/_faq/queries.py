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
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


PROMPT = textwrap.dedent(
    """
        # Overview

        You have been provided with an email transcript.

        It is your job to extract a list of all of the questions,
        queries, as well as any requests for information that are within
        the email transcript. You are required to respond in JSON
        format.

        Make sure that each query includes any information relevant to
        the query from the email. You may have to slightly reword the
        query to achieve this.

        ## The email transcript

        {transcript}

        ## Required JSON format

        [
            "<first-question>",
            "<second-question>",
            ...
            "nth-question"
        ]

        ## An example response

        [
            "At what point during studies does one get to run a franchise?",
            "Age limits for the course",
            "Am I required to pay back the loan during my studies or after, if I do go the loan route?",
            "What is the education component of the program and how is it delivered?"
        ]

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def get_queries(email: Email) -> list[str]:
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

    questions = json.loads(response)

    return questions
