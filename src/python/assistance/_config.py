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


from typing import Literal, TypedDict, cast

import aiofiles
import toml

from assistance._paths import CONFIG

DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
ROOT_DOMAIN = "assistance.chat"
PAYMENT_LINK = "https://buy.stripe.com/bIYeXF2s1d0E4wg9AB"
EMAIL_PRODUCT_ID = "prod_NLuYISl8KZ6fUX"

TargetedNewsFormats = Literal["digest", "discourse"]


class TargetedNewsUserOverrides(TypedDict, total=False):
    delivery_time: str
    delivery_timezone: str
    delivery_frequency: str
    goals: list[str]
    tasks: list[str]


class TargetedNewsSubscriptionDataItem(TypedDict):
    target_audience: str
    sentence_blacklist: list[str]
    keywords: list[str]
    agent_user: str
    format: TargetedNewsFormats
    subscribers: list[str]
    user_overrides: dict[str, TargetedNewsUserOverrides]


class TargetedNewsConfig(TypedDict):
    delivery_time: str
    delivery_timezone: str
    delivery_frequency: str
    goals: list[str]
    goal_weights: list[float]
    tasks: list[str]
    task_weights: list[float]
    subscription_data: list[TargetedNewsSubscriptionDataItem]


def get_google_oauth_client_id():
    return _load_config_item("google-oauth-client-id")


def _load_config_item(name: str):
    path = CONFIG / name

    with open(path, encoding="utf8") as f:
        item = f.read().strip()

    return item


async def load_targeted_news_config() -> TargetedNewsConfig:
    async with aiofiles.open(CONFIG / "targeted-news.toml", "r") as f:
        news_config = cast(TargetedNewsConfig, toml.loads(await f.read()))

    return news_config
