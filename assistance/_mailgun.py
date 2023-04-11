# Copyright (C) 2022 Assistance.Chat contributors

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
import secrets

import aiohttp

from assistance._logging import log_info
from assistance._paths import USERS

from . import _ctx
from ._config import ROOT_DOMAIN
from ._keys import get_mailgun_api_key, get_postal_api_key

EMAIL_SUBJECT = f"Your career.{ROOT_DOMAIN} access link"
EMAIL_TEMPLATE = (
    "Your personal access link, which is tied to your email is {access_link}"
)
LINK_TEMPLATE = "https://career.{domain}/?pwd={password}"

API_KEY = get_mailgun_api_key()
POSTAL_API_KEY = get_postal_api_key()


async def send_email(scope: str, postal_data):
    headers = {
        "Content-Type": "application/json",
        "X-Server-API-Key": POSTAL_API_KEY,
    }

    url = "https://postal.assistance.chat/api/v1/send/message"

    if "cc" in postal_data and postal_data["cc"] == "":
        del postal_data["cc"]

    log_info(scope, json.dumps(postal_data, indent=2))

    postal_response = await _ctx.session.post(
        url=url,
        headers=headers,
        data=json.dumps(postal_data),
    )

    log_info(scope, json.dumps(await postal_response.json(), indent=2))


# async def send_email_with


def get_access_link(email: str):
    try:
        with open(USERS / email, encoding="utf8") as f:
            password = f.read().strip()
    except FileNotFoundError:
        password = secrets.token_urlsafe()

        # We are generating the user passwords. They are not user
        # generated. Therefore we can save the tokens that we generate
        # in plaintext on the secure server.
        with open(USERS / email, "w", encoding="utf8") as f:
            f.write(password)

    return LINK_TEMPLATE.format(password=password, domain=ROOT_DOMAIN)


async def send_access_link(email: str):
    url = f"https://api.eu.mailgun.net/v3/{ROOT_DOMAIN}/messages"

    access_link = get_access_link(email=email)

    data = {
        "from": f"noreply@{ROOT_DOMAIN}",
        "to": email,
        "subject": EMAIL_SUBJECT,
        "text": EMAIL_TEMPLATE.format(access_link=access_link),
    }

    await _ctx.session.post(
        url=url, auth=aiohttp.BasicAuth(login="api", password=API_KEY), data=data
    )
