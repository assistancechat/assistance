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

import aiofiles

from assistance._paths import NEW_GOOGLE_ALERTS, get_article_metadata_path
from assistance._types import Article
from assistance._utilities import get_cleaned_url


async def collect_new_articles() -> tuple[list[str], list[Article]]:
    coroutines = []
    new_alerts = list(NEW_GOOGLE_ALERTS.glob("*"))

    # Group articles that appeared at a similar time together so that
    # the similar articles are more likely to appear in the same
    # chunk.
    # Has the extra benefit of having a deterministic order, allowing
    # for the lru cache to be more efficient.
    new_alerts_hashes = [
        item.name for item in sorted(new_alerts, key=lambda x: x.stat().st_mtime)
    ]

    for alert_hash in new_alerts_hashes:
        coroutines.append(_collect_articles_from_alert(alert_hash))

    articles = dict(await asyncio.gather(*coroutines))

    sorted_articles = []
    for alert_hash in new_alerts_hashes:
        sorted_articles.append(articles[alert_hash])

    return new_alerts_hashes, sorted_articles


async def _collect_articles_from_alert(hash_digest: str) -> tuple[str, Article]:
    article_path = get_article_metadata_path(hash_digest)

    async with aiofiles.open(article_path, "r") as f:
        article_details = json.loads(await f.read())

    article_details["url"] = get_cleaned_url(article_details["url"])

    return hash_digest, article_details
