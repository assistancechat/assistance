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
import pathlib

import aiofiles

from ._paths import ARTICLES, NEW_GOOGLE_ALERTS, get_article_path


async def collect_new_articles():
    coroutines = []
    new_alerts = NEW_GOOGLE_ALERTS.glob("*")

    for alert in new_alerts:
        coroutines.append(_collect_articles_from_alert(alert.name))

    articles = await asyncio.gather(*coroutines)

    return articles


async def _collect_articles_from_alert(hash_digest: str):
    article_path = get_article_path(hash_digest)

    async with aiofiles.open(article_path, "r") as f:
        article_details = json.loads(await f.read())

    return article_details
