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

from assistance._config import load_faq_data
from assistance._embeddings import get_top_questions_and_answers
from assistance._keys import get_openai_api_key

import asyncio
import random
import json
import re
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo

from mailparser_reply import EmailReplyParser

from assistance import _ctx
from assistance._openai import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._summarisation.thread import run_with_summary_fallback
from assistance._tooling.executive_function_system import get_tools_and_responses
from assistance._types import Email
from assistance._config import load_faq_data
from .extract_questions import get_questions
from assistance._utilities import items_to_list_string
from assistance._utilities import get_cleaned_email

from assistance._openai import get_completion_only
from .sub_questions import get_questions
from .batched_questions import get_questions_by_batch


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
        # Answering a prospective student's question

        You have been forwarded an email from Alex Carpenter. A
        prospective student is asking him questions about Jim's
        International Pathway Program. You are happy to help answer any
        questions that the prospective student may have about the Jim's
        International Pathway Program.

        Within their email the prospective student has asked a question.
        You are to draft Alex's answer to the question. Below are a
        range of previous FAQ responses that Alex has provided to other
        students. Use these FAQ responses as a guide to help you draft
        your own response.

        Do not use any of your outside knowledge to help you draft your
        response. Only use the information provided to you within the
        previous FAQ responses. If no FAQ responses is relevant to the
        question, then ONLY respond with an empty string.

        ## Question asked by THIS applicant

        {question}

        ## Previous responses to OTHER prospective students

        These questions are not necessarily the same as the question
        asked by this prospective student.

        {faq_responses}

        ## Your answer

        Q: {question}
        A:
    """
).strip()

RANK = textwrap.dedent(
    """
        # Select best answer

        You have been forwarded an email from Alex Carpenter. A
        prospective student is asking him questions about Jim's
        International Pathway Program. You are happy to help answer any
        questions that the prospective student may have about the Jim's
        International Pathway Program.

        Within their email the prospective student has asked a question.
        You have also been provide with a list of possible answers. You
        are to select the best answer to the question from the list of
        answers.

        You are required to select the answer that both, best answers
        the original question, but also best aligns with the responses
        within the FAQ provided.

        Your response is required to be the id of the answer itself
        ONLY.

        If no response meets the required answers standard then set the
        "does any response meet the required standard?" field to false.

        ## Previous responses to OTHER prospective students

        These questions are not necessarily the same as the question
        asked by this prospective student.

        {faq_responses}

        ## Question asked by THIS applicant

        {question}

        ## Answers to THIS applicant's question to choose from

        {answers}

        ## Required JSON format

        {{
            "does any response meet the required standard?": <true or false>,
            "id of the best answer": <id>,
            "does the selected answer completely answer the user's question?": <true or false>
        }}

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def write_answer(
    scope: str,
    faq_data,
    question: str,
):
    questions = await get_questions(scope=scope, question=question)

    # Don't need to batch the questions for this use case
    # questions_by_batch = await get_questions_by_batch(scope=scope, questions=questions)

    faq_responses = await get_top_questions_and_answers(
        openai_api_key=OPEN_AI_API_KEY, faq_data=faq_data, queries=questions
    )

    sorted_faq_responses = faq_responses.copy()

    coroutines = []
    for _ in range(10):
        random.shuffle(faq_responses)
        coroutines.append(
            get_completion_only(
                scope=scope,
                prompt=PROMPT.format(
                    question=question, faq_responses="\n\n".join(faq_responses)
                ),
                api_key=OPEN_AI_API_KEY,
                **MODEL_KWARGS,
            )
        )

    question_responses = await asyncio.gather(*coroutines)

    log_info(scope, json.dumps(question_responses, indent=2))

    if "" in question_responses:
        return ""

    question_responses_with_id = []
    for i, response in enumerate(question_responses):
        question_responses_with_id.append({"id": i, "answer": response})

    response = await get_completion_only(
        scope=scope,
        prompt=RANK.format(
            question=question,
            faq_responses="\n\n".join(sorted_faq_responses),
            answers=json.dumps(question_responses_with_id, indent=2),
        ),
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    response_data = json.loads(response)
    if (
        not response_data["does any response meet the required standard?"]
        or not response_data[
            "does the selected answer completely answer the user's question?"
        ]
    ):
        return ""

    best_answer_id = response_data["id of the best answer"]

    return question_responses[int(best_answer_id)]
