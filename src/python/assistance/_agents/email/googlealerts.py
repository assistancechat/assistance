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


import textwrap

from assistance._agents.relevance import get_most_relevant_articles
from assistance._agents.summaries import summarise_url_with_tasks
from assistance._keys import get_openai_api_key
from assistance._parsing.googlealerts import parse_alerts

from .types import Email

OPEN_AI_API_KEY = get_openai_api_key()


NUM_OF_ARTICLES_TO_SELECT = 3
TASKS = [
    "Write a paragraph that provides an overview of the main point of this article",
    'Write a paragraph answering the question "Why is this information important for international students to know?"',
    "Provide a discussion provoking question based on this article",
]

PROMPT = textwrap.dedent(
    """
        You are aiming to write {num_tasks} paragraphs about a
        section of text that you have been provided.

        For each of the {num_tasks} below write a paragraph addressing
        that task:

        {tasks}

        Fulfil these tasks for the following text:

        {text}

        Your {num_tasks} paragraphs:
    """
).strip()


async def googlealerts_agent(email: Email):
    article_details = parse_alerts(email["body-html"])

    most_relevant_articles = get_most_relevant_articles(
        openai_api_key=OPEN_AI_API_KEY,
        articles=article_details,
        tasks=TASKS,
        num_of_articles_to_select=NUM_OF_ARTICLES_TO_SELECT,
    )

    for article in most_relevant_articles:
        url = article["url"]
        summary = summarise_url_with_tasks(
            openai_api_key=OPEN_AI_API_KEY, url=url, tasks=TASKS
        )
        print(summary)
