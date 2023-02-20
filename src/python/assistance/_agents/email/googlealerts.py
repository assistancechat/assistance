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
import hashlib
import json
import logging
import textwrap
from urllib.parse import parse_qs, urlparse

import aiofiles

from assistance._agents.relevance import get_most_relevant_articles
from assistance._agents.summaries import summarise_url_with_tasks
from assistance._completions import completion_with_back_off
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key
from assistance._mailgun import send_email
from assistance._parsing.googlealerts import parse_alerts
from assistance._paths import ARTICLES, GOOGLE_ALERTS_PIPELINES

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


TASKS = [
    "Write a paragraph that provides an overview of the main point of this article",
    "Write a paragraph answering why this information is important for your target audience",
    "Provide a discussion provoking question based on this article",
]

TARGET_AUDIENCE = "international students who are studying within Australia"

PROMPT = textwrap.dedent(
    """
        You are aiming to write an engaging and truthful social media
        post about an article of text that you have been provided while
        fulfilling a series of detailed tasks.

        You are not aiming to sell anything, instead just be
        informative. If the article is a "puff piece" make sure not to
        buy into the hype. Instead, be truthful and provide a balanced
        view while still being enthusiastic in your writing and making
        your post interesting and engaging.

        Your primary goal is to develop discussion and engagement with
        your audience around your post.

        If there isn't ample information within the article
        to work from set "article-relevant-to-tasks" to false.

        Make sure your post contains all the relevant information
        regarding the tasks. The reader should not need to read the
        article. Nor are you wanting them to actually read the article.

        Fulfil each task in its own paragraph.

        The target audience for your post is:

        {target_audience}

        Within your post you are aiming to fulfil the following tasks:

        {tasks}

        The article of text you have been provided is:

        {text}

        Required JSON response format:

        {{
            "article-relevant-to-tasks": [true or false],
            "subject": "<Post subject goes here>",
            "content": "<Post content goes here, include new lines as \\n>"
        }}

        JSON response:
    """
).strip()


async def googlealerts_agent(email: Email):
    article_details = parse_alerts(email["body-html"])

    new_alerts_path = GOOGLE_ALERTS_PIPELINES / "new-alert-articles"

    for item in article_details:
        details_for_saving = {"subject": email["subject"], **item}

        single_article_details_as_string = json.dumps(
            details_for_saving, indent=2, sort_keys=True
        )
        hash_digest: str = hashlib.sha224(
            single_article_details_as_string.encode("utf-8")
        ).hexdigest()

        article_path = (
            ARTICLES / hash_digest[0:4] / hash_digest[4:8] / f"{hash_digest}.json"
        )
        article_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(article_path, "w") as f:
            await f.write(single_article_details_as_string)

        pipeline_path = new_alerts_path / hash_digest
        async with aiofiles.open(pipeline_path, "w") as f:
            pass

    # user_email = email["user-email"]

    # logging.info(json.dumps(article_details, indent=2))

    # most_relevant_articles = await get_most_relevant_articles(
    #     user_email=user_email,
    #     openai_api_key=OPEN_AI_API_KEY,
    #     articles=article_details,
    #     tasks=TASKS,
    #     num_of_articles_to_select=5,
    #     keys=["title", "description"],
    # )

    # for article in most_relevant_articles:
    #     parsed_url = urlparse(article["url"])
    #     cleaned_url = parse_qs(parsed_url.query)["url"][0]
    #     article["cleaned_url"] = cleaned_url

    # coroutines = []
    # for article in most_relevant_articles:
    #     url = article["cleaned_url"]
    #     cached_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}&strip=1&vwsrc=0"

    #     coroutines.append(
    #         _summarise_and_fulfil_tasks(
    #             user_email=user_email,
    #             openai_api_key=OPEN_AI_API_KEY,
    #             tasks=TASKS,
    #             url=cached_url,
    #         )
    #     )

    # results = await asyncio.gather(*coroutines)

    # all_relevant_responses = []
    # for article, result in zip(most_relevant_articles, results):
    #     result_data = json.loads(result, strict=False)

    #     if not result_data["article-relevant-to-tasks"]:
    #         continue

    #     all_relevant_responses.append(
    #         {
    #             "title": article["title"],
    #             "url": article["cleaned_url"],
    #             "subject": result_data["subject"],
    #             "content": result_data["content"],
    #         }
    #     )

    # most_relevant_responses = await get_most_relevant_articles(
    #     openai_api_key=OPEN_AI_API_KEY,
    #     articles=all_relevant_responses,
    #     tasks=TASKS,
    #     num_of_articles_to_select=3,
    #     keys=["title", "subject", "description"],
    # )

    # for response in most_relevant_responses:
    #     text = f"{response['content']}\n\n{response['url']}"
    #     mailgun_data = {
    #         "from": f"{email['agent-name']}@{ROOT_DOMAIN}",
    #         "to": email["user-email"],
    #         "subject": response["subject"],
    #         "text": text,
    #     }

    #     asyncio.create_task(send_email(mailgun_data))


async def _summarise_and_fulfil_tasks(
    user_email: str, openai_api_key: str, tasks: list[str], url: str
) -> str:
    summary = await summarise_url_with_tasks(
        user_email=user_email, openai_api_key=openai_api_key, url=url, tasks=tasks
    )

    tasks_string = textwrap.indent("\n".join(tasks), "- ")

    prompt = PROMPT.format(
        num_tasks=len(tasks),
        tasks=tasks_string,
        text=summary,
        target_audience=TARGET_AUDIENCE,
    )

    completions = await completion_with_back_off(
        user_email=user_email, prompt=prompt, api_key=openai_api_key, **MODEL_KWARGS
    )
    response: str = completions.choices[0].text.strip()

    return response
