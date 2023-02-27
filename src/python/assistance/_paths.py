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

import hashlib
import pathlib

import aiofiles

LIB = pathlib.Path(__file__).parent

STORE = pathlib.Path.home().joinpath(".assistance")
CONFIG = STORE.joinpath("config")
SECRETS = CONFIG.joinpath("secrets")

USERS = STORE.joinpath("users")
EMAIL_MAPPING = USERS.joinpath("email-mapping")
USER_DETAILS = USERS.joinpath("details")
AGENT_MAPPING = USERS.joinpath("agent-mapping")

RECORDS = STORE.joinpath("records")

PROMPTS = RECORDS.joinpath("prompts")
COMPLETIONS = RECORDS.joinpath("completions")
ARTICLE_METADATA = RECORDS.joinpath("article-metadata")
DOWNLOADED_ARTICLES = RECORDS.joinpath("downloaded-articles")
EMAILS = RECORDS.joinpath("emails")

PIPELINES = STORE.joinpath("pipelines")

GOOGLE_ALERTS_PIPELINES = PIPELINES.joinpath("google-alerts")
NEW_GOOGLE_ALERTS = GOOGLE_ALERTS_PIPELINES.joinpath("new")

EMAIL_PIPELINES = PIPELINES.joinpath("emails")
NEW_EMAILS = EMAIL_PIPELINES.joinpath("new")


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


async def _get_file_based_mapping(root: pathlib.Path, user: str):
    user_details_files = (root / user).glob("*")

    details = {"user": user}

    for file in user_details_files:
        assert file.name != "user"

        async with aiofiles.open(file) as f:
            details[file.name] = (await f.read()).strip()

    return details


def get_article_metadata_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(ARTICLE_METADATA, hash_digest, create_parent)

    return path


def get_downloaded_article_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(DOWNLOADED_ARTICLES, hash_digest, create_parent)

    return path


def get_emails_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(EMAILS, hash_digest, create_parent)

    return path


def get_hash_digest(text: str) -> str:
    return hashlib.sha224(text.encode("utf-8")).hexdigest()


def _get_record_path(root: pathlib.Path, hash_digest: str, create_parent: bool):
    path = root / _get_relative_json_path(hash_digest)

    if create_parent:
        path.parent.mkdir(parents=True, exist_ok=True)

    return path


def _get_relative_json_path(hash_digest: str):
    return pathlib.Path(hash_digest[0:4]) / hash_digest[4:8] / f"{hash_digest}.json"
