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
import logging
import textwrap
from urllib.parse import parse_qs, urlparse

from assistance._agents.relevance import get_most_relevant_articles
from assistance._agents.summaries import summarise_url_with_tasks
from assistance._completions import completion_with_back_off
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key
from assistance._mailgun import send_email
from assistance._parsing.googlealerts import parse_alerts

from .reply import create_reply
from .types import Email

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 512,
    "best_of": 1,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}

OPEN_AI_API_KEY = get_openai_api_key()


NUM_OF_ARTICLES_TO_SELECT = 3
TASKS = [
    "Write a paragraph that provides an overview of the main point of this article",
    'Write a paragraph answering the question "Why is this information important for international students to know?"',
    "Provide a discussion provoking question based on this article",
]

PROMPT = textwrap.dedent(
    """
        You are aiming to write an engaging and truthful social media
        post about an article of text that you have been provided.

        The target audience are international students who are studying
        within Australia.

        You are not aiming to sell anything, instead just be informative.
        If there isn't ample information within the article to work from
        simply respond with NOT_RELEVANT.

        If the text you have been provided is NOT_RELEVANT do not create
        a post.

        Within you post you are aiming to fulfil the following tasks:

        {tasks}

        The article of text you have been provided is:

        {text}

        Your post:
    """
).strip()


async def googlealerts_agent(email: Email):
    article_details = parse_alerts(email["body-html"])

    logging.info(json.dumps(article_details, indent=2))

    most_relevant_articles = await get_most_relevant_articles(
        openai_api_key=OPEN_AI_API_KEY,
        articles=article_details,
        tasks=TASKS,
        num_of_articles_to_select=NUM_OF_ARTICLES_TO_SELECT,
    )

    for article in most_relevant_articles:
        parsed_url = urlparse(article["url"])
        cleaned_url = parse_qs(parsed_url.query)["url"][0]
        article["cleaned_url"] = cleaned_url

    coroutines = []
    for article in most_relevant_articles:
        url = article["cleaned_url"]
        cached_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}&strip=1&vwsrc=0"

        coroutines.append(
            _summarise_and_fulfil_tasks(
                openai_api_key=OPEN_AI_API_KEY,
                tasks=TASKS,
                url=cached_url,
            )
        )

    results = await asyncio.gather(*coroutines)

    responses = []
    for article, result in zip(most_relevant_articles, results):
        if "NOT_RELEVANT" in result:
            continue

        responses.append(f"{article['title']}\n{article['cleaned_url']}\n\n{result}")

    response = "\n\n\n".join(responses)

    subject, _total_reply = create_reply(
        subject=email["subject"],
        body_plain=email["body-plain"],
        response=response,
        user_email=email["user-email"],
    )

    mailgun_data = {
        "from": f"{email['agent-name']}@{ROOT_DOMAIN}",
        "to": email["user-email"],
        "subject": subject,
        "text": response,
    }

    await send_email(mailgun_data)


async def _summarise_and_fulfil_tasks(
    openai_api_key: str, tasks: list[str], url: str
) -> str:
    summary = await summarise_url_with_tasks(
        openai_api_key=openai_api_key, url=url, tasks=tasks
    )

    tasks_string = textwrap.indent("\n".join(tasks), "- ")

    prompt = PROMPT.format(num_tasks=len(tasks), tasks=tasks_string, text=summary)

    completions = await completion_with_back_off(
        prompt=prompt, api_key=openai_api_key, **MODEL_KWARGS
    )
    response: str = completions.choices[0].text.strip()

    return response
