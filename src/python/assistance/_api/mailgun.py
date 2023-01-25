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

import secrets

import aiohttp

from assistance._paths import USERS

from . import ctx
from .keys import get_mailgun_api_key

EMAIL_SUBJECT = "Your career.assistance.chat access link"
EMAIL_TEMPLATE = (
    "Your personal access link, which is tied to your email is {access_link}"
)
LINK_TEMPLATE = "https://career.assistance.chat/?pwd={password}"

API_KEY = get_mailgun_api_key()
DOMAIN = "assistance.chat"


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

    return LINK_TEMPLATE.format(password=password)


async def send_access_link(email: str):
    url = f"https://api.eu.mailgun.net/v3/{DOMAIN}/messages"

    access_link = get_access_link(email=email)

    data = {
        "from": "noreply@assistance.chat",
        "to": email,
        "subject": EMAIL_SUBJECT,
        "text": EMAIL_TEMPLATE.format(access_link=access_link),
    }

    await ctx.session.post(
        url=url, auth=aiohttp.BasicAuth(login="api", password=API_KEY), data=data
    )
