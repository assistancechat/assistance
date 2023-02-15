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

from assistance._completions import completion_with_back_off
from assistance._vendor.stackoverflow.web_scraping import scrape

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
        helping someone fulfil the following tasks across the whole set
        of articles:

        {tasks}

        Below are {num_of_articles} articles that may be relevant to the
        tasks. Provide the id of the {num_of_articles_to_select} most
        relevant articles to the tasks as a Python list.

        Do not answer the tasks themselves. Instead, ONLY provide the
        ids of the articles that you think would be help someone else
        best at fulfil those tasks.

        Required format:

        [<id of most relevant article>, <id of second most relevant article>, ...]

        Articles:

        {articles}

        {num_of_articles_to_select} most relevant article ids:
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

        try:
            article_ids = json.loads(response)
            break
        except json.JSONDecodeError:
            pass

    if not article_ids:
        raise ValueError("Could not parse article ids")

    top_articles = []
    for article_id in article_ids:
        top_articles.append(articles[article_id])

    logging.info(f"Top articles: {json.dumps(top_articles, indent=2)}")

    return top_articles
