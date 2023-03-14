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
        # Extraction of Questions about Jim's International Pathway Program

        You have been provided with an email transcript where a range
        of questions about the Jim's International Pathway Program and
        its application process have been asked.

        It is your job to extract a full and complete list of all of the
        questions, queries, as well as any requests for information that
        are within the email transcript that are related to the program
        or its application.

        Make sure to include any relevant contextual information from
        the email transcript around why the user is asking the question.
        In particular, make sure to include information around the focus
        of the question being asked.

        Include at the end of the context a re-wording of the question
        in your own words. Making sure to highlight any key components
        of the question that you think are important.

        Do not reword the question, provide the question as is it was
        originally written.

        If somewhere within the transcript the question has already been
        answered then provide the answer within the "extracted answer"
        field.

        If the question has not been answered yet, leave the "extracted answer"
        field blank with an empty string ("").

        ## The email transcript

        {transcript}

        ## Required JSON format

        [
            {{
                "question": "<first question>",
                "context": "<Any relevant context from the email transcript>",
                "extracted answer": "<The answer given in the transcript>",
                "step by step reasoning for whether or not the extracted answer completely answers the user's question": "<Your reasoning>",
                "does this extracted answer completely answer the user's question?": <true or false>,
                "was this question asked after the given answer": <true or false>
            }},
            {{
                "question": "<second question>",
                "context": "<Any relevant context from the email transcript>",
                "extracted answer": "<The answer given in the transcript>",
                "step by step reasoning for whether or not the extracted answer completely answers the user's question": "<Your reasoning>",
                "does this extracted answer completely answer the user's question?": <true or false>,
                "was this question asked after the given answer": <true or false>
            }},
            ...
            {{
                "question": "<nth question>",
                "context": "<Any relevant context from the email transcript>",
                "extracted answer": "<The answer given in the transcript>",
                "step by step reasoning for whether or not the extracted answer completely answers the user's question": "<Your reasoning>",
                "does this extracted answer completely answer the user's question?": <true or false>,
                "was this question asked after the given answer": <true or false>
            }}
        ]

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


SUMMARY_INSTRUCTIONS = textwrap.dedent(
    """
        When summarising the email thread, please make sure to include
        any questions that was asked within the email thread as well as
        any answers that were given, as well as any contextual
        information around the question and answer itself.
    """
).strip()


class QuestionAndContext(TypedDict):
    question: str
    context: str
    answer: str
    answer_again: bool


async def extract_questions(email: Email) -> list[QuestionAndContext]:
    scope = email["user_email"]

    email_thread = get_email_thread(email)

    # last_two_emails_thread = email_thread[-2:]

    response = await run_with_summary_fallback(
        scope=scope,
        prompt=PROMPT,
        instructions="",
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    questions = json.loads(response)

    for question in questions:
        question["answer"] = question["extracted answer"]
        del question["extracted answer"]

        question["answer_again"] = (
            not question[
                "does this extracted answer completely answer the user's question?"
            ]
            or question["was this question asked after the given answer"]
        )
        del question[
            "does this extracted answer completely answer the user's question?"
        ]
        del question["was this question asked after the given answer"]

    return questions
