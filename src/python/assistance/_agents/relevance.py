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

from assistance import _ctx
from assistance._completions import completion_with_back_off

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 512,
    "best_of": 1,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

PROMPT = textwrap.dedent(
    """
        You are aiming to find the articles that might be the best at
        helping someone fulfil the following tasks:

        {tasks}

        Below are {num_of_articles} articles that may be relevant to the
        tasks. Provide the id of the {num_of_articles_to_select} most
        relevant articles to the tasks as a Python list.

        Do not complete the tasks themselves. Instead, ONLY provide the
        ids of the articles that you think would be the most helpful for
        someone else to fulfil those tasks.

        For each article that you select, provide an absolute score
        between 0 and 100. The score is a measure of how relevant you
        think the article is to achieving the tasks.

        Required JSON format:

        {{
            "scores": [<score of most relevant article>, <score of second most relevant article>, ...],
            "ids": [<id of most relevant article>, <id of second most relevant article>, ...]
        }}

        Articles:

        {articles}

        JSON response:
    """
).strip()


async def get_most_relevant_articles(
    openai_api_key: str,
    tasks: list[str],
    articles: list[dict[str, str]],
    num_of_articles_to_select: int,
):
    tasks_string = textwrap.indent("\n".join(tasks), "- ")

    articles_with_ids = []
    for index, article in enumerate(articles):
        articles_with_ids.append({"id": index, **article})

    logging.info(_ctx.pp.pprint(articles_with_ids))

    article_ids: None | list[int] = None
    for _ in range(3):
        prompt = PROMPT.format(
            tasks=tasks_string,
            num_of_articles=len(articles),
            num_of_articles_to_select=num_of_articles_to_select,
            articles=json.dumps(articles_with_ids, indent=2),
        )

        completions = await completion_with_back_off(
            prompt=prompt, api_key=openai_api_key, **MODEL_KWARGS
        )
        response: str = completions.choices[0].text.strip()

        logging.info(f"Response: {response}")

        try:
            article_ranking = json.loads(response)
            article_ids = article_ranking["ids"]
            article_scores = article_ranking["scores"]

            break
        except (json.JSONDecodeError, KeyError) as e:
            logging.info(e)

    if not article_ids:
        raise ValueError("Could not parse article ids")

    top_articles = []
    for i, article_id in enumerate(article_ids):
        article = articles[article_id]
        article["score"] = article_scores[i]

        top_articles.append(article)

    logging.info(f"Top articles: {_ctx.pp.pprint(top_articles)}")

    return top_articles
