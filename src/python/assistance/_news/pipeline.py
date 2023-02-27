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

from assistance._agents.relevance import article_scoring
from assistance._agents.summaries import summarise_news_article_url_with_tasks
from assistance._completions import completion_with_back_off
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key
from assistance._mailgun import send_email
from assistance._parsing.googlealerts import parse_alerts
from assistance._paths import (
    ARTICLE_METADATA,
    NEW_GOOGLE_ALERTS,
    get_article_metadata_path,
    get_hash_digest,
)
from assistance._types import Email


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
