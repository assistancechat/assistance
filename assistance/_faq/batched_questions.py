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

        You have been provided with a list of questions. You are to
        determine if there are any questions that would be benefited by
        having another question answered first.

        Provide a list of all the question ids that would be of benefit
        to the current question, and therefore should be asked before
        the current question.

        If there would be no questions that would be benefited the
        current question, then you should respond with an empty list.

        ## The list of questions

        {questions}

        ## Required JSON format

        [
            {{
                "id": 0,
                "think step by step": "<step by step reasoning>",
                "questions that should be asked before this one": [<first question id>, <second question id>, ..., <ith question id>]
            }},
            {{
                "id": 1,
                "think step by step": "<step by step reasoning>",
                "questions that should be asked before this one": [<first question id>, <second question id>, ..., <ith question id>]
            }},
            ...
            {{
                "id": <n - 1>,
                "think step by step": "<step by step reasoning>",
                "questions that should be asked before this one": [<first question id>, <second question id>, ..., <ith question id>>]
            }}
        ]

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def get_questions_by_batch(scope: str, questions: list[str]) -> list[str]:
    questions_with_id = []
    for i, question in enumerate(questions):
        questions_with_id.append({"id": i, "question": question})

    response = await get_completion_only(
        scope=scope,
        prompt=PROMPT.format(questions=json.dumps(questions_with_id, indent=4)),
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    dependency_tree = json.loads(response)

    questions_by_batch = []
    question_ids_included = set()
    all_question_ids = set(range(len(questions)))
    all_dependencies = [
        item["questions that should be asked before this one"]
        for item in dependency_tree
    ]

    while question_ids_included != all_question_ids:
        questions_in_order = []
        questions_ids_in_previous_batch = question_ids_included.copy()

        for i, (question, current_dependencies) in enumerate(
            zip(questions, all_dependencies)
        ):
            if i in question_ids_included:
                continue

            if set(current_dependencies).issubset(questions_ids_in_previous_batch):
                question_ids_included.add(i)
                questions_in_order.append(question)

        questions_by_batch.append(questions_in_order)

    return questions_by_batch
