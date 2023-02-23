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
import logging
import textwrap
from typing import TypedDict

from assistance import _ctx
from assistance._completions import completion_with_back_off
from assistance._utilities import items_to_list_string

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 1536,
    "best_of": 1,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

MAX_ARTICLE_COUNT = 24

PROMPT = textwrap.dedent(
    """
        You are aiming to find the articles that might be the best at
        helping someone fulfil the following tasks and goals for their
        target audience:

        Their tasks:

        {tasks}

        Their goals:

        {goals}

        Their target audience:

        {target_audience}

        Your instructions:

        Below are {num_of_articles} articles that may be relevant to the
        tasks and goal. For each article id provide a score between 0
        and 10 for each goal and task for their target audience. The
        scores are a measure of how helpful you think the article will
        be in achieving each respective task and goal.

        For each article, if there are other articles within the list
        that are covering a very similar topic, provide those articles
        as a "similar-topic-covered" list. If no other articles are
        covering a similar topic, provide an empty list.

        Required JSON format:

        [
            {{
                "id": 1,
                "task-scores": [<provide the relevance score for the first task>, <provide the relevance score for the second task>, ...],
                "goal-scores": [<provide the relevance score for the first goal>, ...],
                "similar-topic-covered": [<provide the article id of the first article that is covering a similar topic as this article>, <second similar article>, ...]
            }},
            {{
                "id": 2,
                ...
            }},

            ...

            {{
                "id": {num_of_articles},
                ...
            }}
        ]

        Articles:

        {articles}

        JSON response:
    """
).strip()


# TODO: Make article scoring handle article length larger than available
# tokens.

# TODO: Adjust max tokens to be a reasonable number given a maximum
# number of articles.


async def article_scoring(
    user_email: str,
    openai_api_key: str,
    goals: list[str],
    tasks: list[str],
    target_audience: str,
    articles: list[dict[str, str]],
    keys: list[str],
):
    articles_with_ids = []
    for index, article in enumerate(articles):
        article_for_prompt: dict[str, int | str] = {"id": index + 1}

        for key in keys:
            article_for_prompt[key] = article[key]

        articles_with_ids.append(article_for_prompt)

    logging.info(_ctx.pp.pformat(articles_with_ids))

    article_ranking: None | list[dict] = None
    prompt = PROMPT.format(
        tasks=items_to_list_string(tasks),
        goals=items_to_list_string(goals),
        target_audience=target_audience,
        num_of_articles=len(articles),
        articles=json.dumps(articles_with_ids, indent=2),
    )

    completions = await completion_with_back_off(
        user_email=user_email, prompt=prompt, api_key=openai_api_key, **MODEL_KWARGS
    )
    response: str = completions.choices[0].text.strip()

    logging.info(f"Response: {response}")

    article_ranking = json.loads(response)

    for item in article_ranking:
        assert "id" in item
        assert "task-scores" in item
        assert "goal-scores" in item
        assert "similar-topic-covered" in item

    return article_ranking
