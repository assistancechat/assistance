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


import pathlib

LIB = pathlib.Path(__file__).parent

STORE = pathlib.Path.home().joinpath(".assistance")

MONOREPO = LIB.parent.parent.parent.parent
if MONOREPO.name == "monorepo":
    CONFIG = MONOREPO.joinpath("config")
else:
    CONFIG = STORE.joinpath("config")


SECRETS = CONFIG.joinpath("secrets")

USERS = STORE.joinpath("users")
EMAIL_MAPPING = USERS.joinpath("email-mapping")
USER_DETAILS = USERS.joinpath("details")
AGENT_MAPPING = USERS.joinpath("agent-mapping")
FORM_DATA = USERS.joinpath("forms")
CAMPAIGN_DATA = USERS.joinpath("campaigns")

RECORDS = STORE.joinpath("records")

PROMPTS = RECORDS.joinpath("prompts")
COMPLETIONS = RECORDS.joinpath("completions")
ARTICLE_METADATA = RECORDS.joinpath("article-metadata")
DOWNLOADED_ARTICLES = RECORDS.joinpath("downloaded-articles")
EMAILS = RECORDS.joinpath("emails")
POSTAL = RECORDS.joinpath("postal")
CONTACT_FORM = RECORDS.joinpath("contact-form")
COMPLETION_CACHE = RECORDS.joinpath("completion-cache")

PIPELINES = STORE.joinpath("pipelines")

GOOGLE_ALERTS_PIPELINES = PIPELINES.joinpath("google-alerts")
NEW_GOOGLE_ALERTS = GOOGLE_ALERTS_PIPELINES.joinpath("new")

EMAIL_PIPELINES = PIPELINES.joinpath("emails")
NEW_EMAILS = EMAIL_PIPELINES.joinpath("new")

LOGS = STORE.joinpath("server", "logs")
PHIRHO_LOGS = LOGS.joinpath("phirho")

TEST_DIR = LIB.joinpath("tests")
TESTS_DATA = TEST_DIR.joinpath("data")

FORM_TEMPLATES = CONFIG.joinpath("form-templates")
FAQ_DATA = CONFIG.joinpath("faq")

AI_DIR = LIB.joinpath("_ai")
AI_REGISTRY_DIR = AI_DIR.joinpath("registry")


def get_article_metadata_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(ARTICLE_METADATA, hash_digest, create_parent)

    return path


def get_downloaded_article_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(DOWNLOADED_ARTICLES, hash_digest, create_parent)

    return path


def get_emails_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(EMAILS, hash_digest, create_parent)

    return path


def get_postal_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(POSTAL, hash_digest, create_parent)

    return path


def get_contact_form_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(CONTACT_FORM, hash_digest, create_parent)

    return path


def get_completion_cache_path(hash_digest: str, create_parent: bool = False):
    path = _get_record_path(COMPLETION_CACHE, hash_digest, create_parent)

    return path


def _get_record_path(root: pathlib.Path, hash_digest: str, create_parent: bool):
    path = root / _get_relative_json_path(hash_digest)

    if create_parent:
        path.parent.mkdir(parents=True, exist_ok=True)

    return path


def _get_relative_json_path(hash_digest: str):
    return pathlib.Path(hash_digest[0:4]) / hash_digest[4:8] / f"{hash_digest}.json"
