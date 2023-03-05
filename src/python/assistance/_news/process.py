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
from typing import Any, Coroutine, TypedDict, cast

import numpy as np

from assistance._agents.post import write_news_post
from assistance._agents.relevance import article_scoring
from assistance._config import (
    ROOT_DOMAIN,
    TargetedNewsConfig,
    TargetedNewsSubscriptionDataItem,
)
from assistance._keys import get_openai_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._paths import NEW_GOOGLE_ALERTS
from assistance._types import Article

from .collect import collect_new_articles

OPEN_AI_API_KEY = get_openai_api_key()
MAX_ARTICLES_PER_SCORING = 20

MIN_ARTICLE_COUNT = 6


async def process_articles(
    cfg: TargetedNewsConfig,
    num_articles: int | None = None,
    delete_alerts: bool = True,
    subscriber_override: list[str] | None = None,
):
    articles_by_hash = await collect_new_articles(num_articles)

    number_of_articles_available = len(articles_by_hash.keys())

    if number_of_articles_available < MIN_ARTICLE_COUNT:
        logging.info(
            f"Too few articles to process. Only {number_of_articles_available} articles found.",
        )
        return

    coroutines = []
    article_hashes_to_save_for_tomorrow = []

    for i, subscription_data in enumerate(cfg["subscription_data"]):
        (
            deduped_hashes_for_keyword,
            deduped_articles_for_keyword,
        ) = await _select_unique_articles_by_keyword(
            subscription_data, articles_by_hash
        )

        if len(deduped_articles_for_keyword) < MIN_ARTICLE_COUNT:
            logging.info(
                f"Too few articles to process for keywords {subscription_data['keywords']}. Only {len(deduped_articles_for_keyword)} articles found.",
            )
            article_hashes_to_save_for_tomorrow += deduped_hashes_for_keyword

            continue

        coroutines.append(
            _process_subscription(
                cfg=cfg,
                subscription_data=subscription_data,
                deduped_articles=deduped_articles_for_keyword,
                subscriber_override=subscriber_override,
            )
        )

    await asyncio.gather(*coroutines)

    if delete_alerts:
        for hash in articles_by_hash.keys():
            if hash not in article_hashes_to_save_for_tomorrow:
                (NEW_GOOGLE_ALERTS / hash).unlink()


EMAIL_TEMPLATE = textwrap.dedent(
    """
        Summary of news article
        -----------------------

        {summary}

        Link to article
        ---------------

        {url}

        Things to consider
        ------------------

        {things_to_consider}

        Something to share
        ------------------

        {content}
    """
).strip()


class DetailsForEmail(TypedDict):
    title: str
    url: str
    subject: str
    summary: str
    things_to_consider: str
    content: str


async def _process_subscription(
    cfg: TargetedNewsConfig,
    subscription_data: TargetedNewsSubscriptionDataItem,
    deduped_articles: list[Article],
    subscriber_override: list[str] | None = None,
):
    scope = subscription_data["agent_user"]

    top_articles = await _get_top_articles(
        cfg=cfg,
        subscription_data=subscription_data,
        deduped_articles=deduped_articles,
    )

    write_news_post_coroutines: list[Coroutine[Any, Any, tuple[str, str]]] = []
    for article in top_articles:
        url = article["url"]

        write_news_post_coroutines.append(
            write_news_post(
                scope=scope,
                openai_api_key=OPEN_AI_API_KEY,
                goals=cfg["goals"],
                tasks=cfg["tasks"],
                target_audience=subscription_data["target_audience"],
                sentence_blacklist=subscription_data["sentence_blacklist"],
                url=url,
                use_google_cache=False,
            )
        )

    results = await asyncio.gather(*write_news_post_coroutines)

    all_relevant_responses: list[DetailsForEmail] = []
    for article, (summary, result) in zip(top_articles, results):
        try:
            result_data = json.loads(result, strict=False)
        except json.JSONDecodeError:
            log_info(scope, f"Failed to decode JSON: {result}")
            continue

        if not result_data["article_is_relevant"]:
            continue

        all_relevant_responses.append(
            {
                "title": article["title"],
                "url": article["url"],
                "subject": result_data["subject"],
                "summary": summary.replace("NOT_RELEVANT", "").strip(),
                "things_to_consider": result_data["things_to_consider"],
                "content": result_data["content"],
            }
        )

    article_scores = await article_scoring(
        scope=scope,
        openai_api_key=OPEN_AI_API_KEY,
        goals=cfg["goals"],
        tasks=cfg["tasks"],
        target_audience=subscription_data["target_audience"],
        articles=cast(list[dict[str, str]], all_relevant_responses),
        keys=["subject", "content"],
    )

    top_scoring_indices = _get_top_scoring_article_indices(
        cfg=cfg, article_scores=article_scores, k=3
    )

    top_scoring_posts: list[DetailsForEmail] = []
    for i in top_scoring_indices:
        top_scoring_posts.append(all_relevant_responses[i])

    if subscriber_override is not None:
        subscribers_to_use = subscriber_override
    else:
        subscribers_to_use = subscription_data["subscribers"]

    send_email_coroutines: list[Coroutine[Any, Any, None]] = []

    digest_email = f"News digest for:\n{subscription_data['target_audience']}\n\n"
    discourse_emails = []

    for i, response in enumerate(top_scoring_posts):
        text = EMAIL_TEMPLATE.format(**response)
        digest_email += f"Article {i + 1})\n{text}\n\n-------------------------\n\n"

        discourse_emails.append(
            {
                "subject": response["subject"],
                "plain_body": text,
            }
        )

    for subscriber in subscribers_to_use:
        agent_user = subscription_data["agent_user"]

        # Done inside the loop as in the future want to be able to
        # handle per user overrides.
        if subscription_data["format"] == "digest":
            postal_data = {
                "from": f"{agent_user}@{ROOT_DOMAIN}",
                "to": [subscriber],
                "subject": "Targeted News Digest",
                "plain_body": digest_email,
            }

            send_email_coroutines.append(send_email(scope, postal_data))
        else:
            for email in discourse_emails:
                postal_data = {
                    "from": f"{agent_user}@{ROOT_DOMAIN}",
                    "to": [subscriber],
                    "subject": email["subject"],
                    "plain_body": email["plain_body"],
                }

                send_email_coroutines.append(send_email(scope, postal_data))

    await asyncio.gather(*send_email_coroutines)


async def _get_top_articles(
    cfg: TargetedNewsConfig,
    subscription_data: TargetedNewsSubscriptionDataItem,
    deduped_articles: list[Article],
    k=6,
) -> list[Article]:
    article_scores = await article_scoring(
        scope=subscription_data["agent_user"],
        openai_api_key=OPEN_AI_API_KEY,
        goals=cfg["goals"],
        tasks=cfg["tasks"],
        target_audience=subscription_data["target_audience"],
        articles=cast(list[dict[str, str]], deduped_articles),
        keys=["description", "title"],
    )

    top_scoring_indices = _get_top_scoring_article_indices(
        cfg=cfg, article_scores=article_scores, k=k
    )

    top_articles = []
    for i in top_scoring_indices:
        top_articles.append(deduped_articles[i])

    return top_articles


async def _select_unique_articles_by_keyword(
    subscription_data: TargetedNewsSubscriptionDataItem,
    articles_by_hash: dict[str, Article],
):
    articles_with_keywords: list[tuple[str, Article]] = []

    for article_hash, article in articles_by_hash.items():
        for keyword in subscription_data["keywords"]:
            if keyword.lower() in article["subject"].lower():
                articles_with_keywords.append((article_hash, article))
                break

    deduped_articles: list[Article] = []
    deduped_hashes: list[str] = []
    urls = set()

    for article_hash, article in articles_with_keywords:
        if article["url"] in urls:
            continue

        urls.add(article["url"])
        deduped_articles.append(article)
        deduped_hashes.append(article_hash)

    return deduped_hashes, deduped_articles


def _get_top_scoring_article_indices(cfg: TargetedNewsConfig, article_scores, k):
    if len(article_scores) < k:
        k = len(article_scores)

    weighted_scores = []
    for score in article_scores:
        weighted_score = 0
        for w, s in zip(cfg["goal_weights"], score["goal-scores"]):
            weighted_score += w * s

        for w, s in zip(cfg["task_weights"], score["task-scores"]):
            weighted_score += w * s

        weighted_scores.append(weighted_score)

    weighted_scores = np.array(weighted_scores)

    top_scoring_indices = np.argpartition(weighted_scores, -k)[-k:]

    return top_scoring_indices
