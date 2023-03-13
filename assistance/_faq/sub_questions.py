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
from assistance._keys import get_openai_api_key
from assistance._logging import log_info
from assistance._openai import get_completion_only

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

        You have been provided with a question from a user within an
        email.

        You have access to a question and answer tool that records
        the questions that previous users have asked. You are aiming
        to search through these questions to find the most relevant
        questions that can be used to answer the provided question.

        However, to have the best chance at extracting the relevant
        information it is helpful to split a question into a series of
        sub-questions that can then also be provided to the tool.

        These questions are required to be written from the perspective
        of the user who has sent you this email.

        It is your job to take the provided question and create a series
        of sub-questions that can be to the tool to then aid you in the
        answering of the question.

        Use the "known-facts" key to describe any facts that you
        currently know about the question.

        Use the "think-step-by-step" key to describe the thought process
        that you went through to determine each of the required
        sub-questions.

        If there are no sub-questions required to answer the question,
        then respond with an empty list.

        Make sure that any sub-questions that you provide are relevant
        to the original question.

        Make sure each question only asks one thing at a time.

        ## Required JSON format

        [
            {{
                "known-facts": "<semicolon separated list of relevant known facts>",
                "think-step-by-step": "<step by step thought process for the first required sub-question>",
                "question": "<first sub-question>"
            }},
            {{
                "known-facts": "<semicolon separated list of relevant known facts>",
                "think-step-by-step": "<step by step thought process for the second required sub-question>",
                "question": "<second sub-question>"
            }},
            ...
            {{
                "known-facts": "<semicolon separated list of relevant known facts>",
                "think-step-by-step": "<step by step thought process for the nth required sub-question>",
                "question": "<nth sub-question>"
            }}
        ]

        ## The original question

        {original_question}

        ## The current question

        {question}

        ## Context around the question

        {context}

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def get_sub_questions(
    scope: str,
    question: str,
    context: str,
    collected_questions: set | None = None,
    original_question: str | None = None,
    max_depth=3,
    current_depth=0,
) -> list[str]:
    if current_depth >= max_depth:
        return []

    if collected_questions is None:
        collected_questions = set()

    if original_question is None:
        original_question = question

    question_tree = [question]

    response = await get_completion_only(
        scope=scope,
        prompt=PROMPT.format(
            question=question, original_question=original_question, context=context
        ),
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    sub_questions_response = json.loads(response)
    sub_questions = [item["question"] for item in sub_questions_response]

    # relevant_sub_questions = await get_relevant_sub_questions(
    #     scope, original_question, sub_questions
    # )

    coroutines = []
    for sub_question in sub_questions:
        if sub_question not in collected_questions and sub_question:
            collected_questions.add(sub_question)

            coroutines.append(
                get_sub_questions(
                    scope,
                    question=sub_question,
                    context=context,
                    collected_questions=collected_questions,
                    original_question=original_question,
                    max_depth=max_depth,
                    current_depth=current_depth + 1,
                )
            )

    sub_question_trees = await asyncio.gather(*coroutines)

    for sub_question_tree in sub_question_trees:
        question_tree = [*sub_question_tree, *question_tree]

    log_info(scope, json.dumps(question_tree, indent=2))

    return question_tree
