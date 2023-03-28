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
import pathlib
import tomllib
from typing import Any, Literal, TypedDict, cast

import aiofiles

from assistance._paths import (
    AGENT_MAPPING,
    CONFIG,
    EMAIL_MAPPING,
    FAQ_DATA,
    FORM_DATA,
    FORM_TEMPLATES,
    USER_DETAILS,
)

SIMPLER_OPENAI_MODEL = "gpt-3.5-turbo"
SOTA_OPENAI_MODEL = "gpt-4"

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
        news_config = cast(TargetedNewsConfig, tomllib.loads(await f.read()))

    return news_config


async def get_user_from_email(email_address: str):
    try:
        async with aiofiles.open(EMAIL_MAPPING / email_address) as f:
            user = await f.read()
    except FileNotFoundError as e:
        raise ValueError("User not found") from e

    return user


async def get_user_details(user: str):
    details = await _get_file_based_mapping(USER_DETAILS, user)

    return details


async def get_agent_mappings(user: str):
    details = await _get_file_based_mapping(AGENT_MAPPING, user)

    return details


class ProgressionItem(TypedDict):
    key: str
    task: str
    fields_for_completion: list[str]
    attachment_handler: str | None
    always_run_at_least_once: bool


class FormConfig(TypedDict):
    defaults: dict[str, Any]
    options: dict[str, list[str]]
    progression: list[ProgressionItem]
    field: dict[str, Any]


async def load_form_config(name: str) -> FormConfig:
    async with aiofiles.open(FORM_TEMPLATES / f"{name}.toml", encoding="utf8") as f:
        form_template = cast(FormConfig, tomllib.loads(await f.read()))

    for item in form_template["progression"]:
        if "fields_for_completion" not in item:
            item["fields_for_completion"] = []

        if "attachment_handler" not in item:
            item["attachment_handler"] = None

        if "always_run_at_least_once" not in item:
            item["always_run_at_least_once"] = False

    return form_template


async def load_faq_data(name: str):
    async with aiofiles.open(FAQ_DATA / f"{name}.toml", encoding="utf8") as f:
        data = cast(FormConfig, tomllib.loads(await f.read()))

    return data


class FormItem(TypedDict):
    value: str
    confirmed: bool


async def get_form_entries(form_name: str, user_email: str) -> dict[str, FormItem]:
    file_contents = await _get_form_data(
        form_name=form_name, data_type="entries", user_email=user_email
    )

    del file_contents["empty_files"]

    return file_contents


async def save_form_entries(
    form_name: str, user_email: str, form_entries: dict[str, FormItem]
):
    dir = FORM_DATA / form_name / "entries" / user_email
    dir.mkdir(parents=True, exist_ok=True)

    for key, item in form_entries.items():
        path = dir / f"{key}.json"

        async with aiofiles.open(path, "w") as f:
            await f.write(json.dumps(item))


async def get_complete_form_progression_keys(
    form_name: str, user_email: str
) -> set[str]:
    file_contents = await _get_form_data(
        form_name=form_name, data_type="progression", user_email=user_email
    )

    return file_contents["empty_files"]


async def set_progression_key(form_name: str, user_email: str, key: str):
    path = FORM_DATA / form_name / "progression" / user_email / key

    path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(path, "w"):
        pass


async def _get_form_data(form_name: str, data_type: str, user_email: str):
    results = await _get_file_based_mapping(
        FORM_DATA / form_name / data_type, user_email, include_user=False
    )

    return results


async def _get_file_based_mapping(root: pathlib.Path, user: str, include_user=True):
    user_details_files = (root / user).glob("*")

    details = {}
    empty_files = set()

    if include_user:
        details["user"] = user

    for file in user_details_files:
        assert file.name != "user"

        async with aiofiles.open(file) as f:
            file_contents = (await f.read()).strip()

        if file.name.endswith(".json"):
            details[file.name[:-5]] = json.loads(file_contents)
            continue

        if file_contents == "":
            empty_files.add(file.name)
            continue

        details[file.name] = file_contents

    details["empty_files"] = empty_files

    return details
