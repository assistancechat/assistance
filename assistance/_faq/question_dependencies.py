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

        You are required to provide a relevance score between 0 and 10
        for a series of questions ranking how how relevant they are in
        being able to be used to answer an original question.

        ## The original question

        {original_question}

        ## The sub-questions

        {sub_questions}

        ## Required JSON format

        [
            {{
                "known-facts": "<semicolon separated list of relevant known facts>",
                "think-step-by-step": "<step by step thought process for the first required sub-question>",
                "relevance-score": <number between 0 and 10>
            }},
            {{
                "known-facts": "<semicolon separated list of relevant known facts>",
                "think-step-by-step": "<step by step thought process for the second required sub-question>",
                "relevance-score": <number between 0 and 10>
            }},
            ...
            {{
                "known-facts": "<semicolon separated list of relevant known facts>",
                "think-step-by-step": "<step by step thought process for the nth required sub-question>",
                "relevance-score": <number between 0 and 10>
            }}
        ]

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def get_relevant_sub_questions(
    scope: str,
    original_question: str,
    sub_questions: list[str],
    cut_off: int = 5,
) -> list[str]:
    response = await get_completion_only(
        scope=scope,
        prompt=PROMPT.format(
            original_question=original_question, sub_questions=sub_questions
        ),
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    question_scoring = json.loads(response)

    relevant_sub_questions = [
        question
        for question, response in zip(sub_questions, question_scoring)
        if response["relevance-score"] >= cut_off
    ]

    return relevant_sub_questions
