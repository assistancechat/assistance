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
import random

import aiofiles

from assistance import _ctx
from assistance._parsing.googlealerts import parse_alerts
from assistance._paths import (
    NEW_GOOGLE_ALERTS,
    get_article_metadata_path,
    get_hash_digest,
)
from assistance._types import Article, Email
from assistance._utilities import get_cleaned_url
from assistance._vendor.stackoverflow.web_scraping import scrape


async def add_to_google_alerts_pipeline(email: Email):
    article_details = parse_alerts(email["html_body"])

    for item in article_details:
        details_for_saving = {"subject": email["subject"], **item}

        single_article_details_as_string = json.dumps(
            details_for_saving, indent=2, sort_keys=True
        )

        hash_digest = get_hash_digest(single_article_details_as_string)
        article_path = get_article_metadata_path(hash_digest, create_parent=True)

        async with aiofiles.open(article_path, "w") as f:
            await f.write(single_article_details_as_string)

        pipeline_path = NEW_GOOGLE_ALERTS / hash_digest
        async with aiofiles.open(pipeline_path, "w") as f:
            pass

    # asyncio.create_task(_pre_cache_articles(article_details))


async def _pre_cache_articles(article_details: list[Article]):
    for article in article_details:
        url = get_cleaned_url(article["url"])

        try:
            await scrape(_ctx.session, url)
        except ValueError:
            await asyncio.sleep(random.uniform(300, 600))
            await _pre_cache_articles(article_details)
            break

        await asyncio.sleep(random.uniform(60, 120))
