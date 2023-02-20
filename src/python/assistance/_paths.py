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

LIB = pathlib.Path(__file__).parent

STORE = pathlib.Path.home() / ".assistance"
CONFIG = STORE / "config"
SECRETS = CONFIG / "secrets"

USERS = STORE / "users"
RECORDS = STORE / "records"

PROMPTS = RECORDS / "prompts"
COMPLETIONS = RECORDS / "completions"
ARTICLES = RECORDS / "articles"
EMAILS = RECORDS / "emails"

PIPELINES = STORE / "pipelines"

GOOGLE_ALERTS_PIPELINES = PIPELINES / "google-alerts"
NEW_GOOGLE_ALERTS = GOOGLE_ALERTS_PIPELINES / "new"

EMAIL_PIPELINES = PIPELINES / "email"
NEW_EMAILS = EMAIL_PIPELINES / "new"


def get_article_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(ARTICLES, hash_digest, create_parent)

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
    return pathlib.Path(hash_digest[0:4] / hash_digest[4:8] / f"{hash_digest}.json")
