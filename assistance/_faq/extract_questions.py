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
from typing import TypedDict

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
        # Question and context extraction

        You have been provided with an email transcript.

        It is your job to extract a full and complete list of all of the
        questions, queries, as well as any requests for information that
        are within the email transcript. You are required to respond in
        JSON format.

        Make sure to include any relevant contextual information from
        the email transcript that will be helpful in answering the given
        question with each extracted question.

        You may reword questions as needed to help achieve an accurate
        standalone representation of the question.

        ## The email transcript

        {transcript}

        ## Required JSON format

        [
            {{
                "question": "<first question>",
                "context": "<Any relevant context from the email transcript>"
            }},
            {{
                "question": "<second question>",
                "context": "<Any relevant context from the email transcript>"
            }},
            ...
            {{
                "question": "<nth question>",
                "context": "<Any relevant context from the email transcript>"
            }}
        ]

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


class QuestionAndContext(TypedDict):
    question: str
    context: str


async def extract_questions(email: Email) -> list[QuestionAndContext]:
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
