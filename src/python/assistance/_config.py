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

import aiofiles

from assistance._paths import CONFIG

ROOT_DOMAIN = "assistance.chat"
PAYMENT_LINK = "https://buy.stripe.com/bIYeXF2s1d0E4wg9AB"
EMAIL_PRODUCT_ID = "prod_NLuYISl8KZ6fUX"


def get_google_oauth_client_id():
    return _load_config_item("google-oauth-client-id")


def _load_config_item(name: str):
    path = CONFIG / name

    with open(path, encoding="utf8") as f:
        item = f.read().strip()

    return item


async def load_targeted_news_config():
    async with aiofiles.open(CONFIG / "targeted-news.json", "r") as f:
        news_config = json.loads(await f.read())

    return news_config
