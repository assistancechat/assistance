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


from fastapi import APIRouter, Request
from pydantic import BaseModel

from assistance._keys import get_mailgun_api_key

router = APIRouter(prefix="/contact-us")

EMAIL_SUBJECT = "[Contact Us Form] @ {origin_url} | {first_name} {last_name}"
EMAIL_TEMPLATE = """{first_name} {last_name} has submitted a contact us form on {origin_url}.
Their email is {email} and their phone number is {phone_number}.

They have agreed to the terms and conditions: {agree_to_terms}

Their message is:
{message}

Their referrer tag is: {referrer_tag}
Which has the following content:
{referrer_tag_content}
"""

LINK_TEMPLATE = "https://career.assistance.chat/?pwd={password}"

API_KEY = get_mailgun_api_key()
DOMAIN = "assistance.chat"


class ContactUsData(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str
    agree_to_terms: bool
    referrer_tag: str | None = None


@router.post("")
async def chat(data: ContactUsData, request: Request):
    origin_url = dict(request.scope["headers"]).get(b"referer", b"").decode()


async def send_access_link(email: str):
    url = f"https://api.eu.mailgun.net/v3/{DOMAIN}/messages"

    access_link = get_access_link(email=email)

    data = {
        "from": "noreply@assistance.chat",
        "to": email,
        "subject": EMAIL_SUBJECT,
        "text": EMAIL_TEMPLATE.format(access_link=access_link),
    }

    await _ctx.session.post(
        url=url, auth=aiohttp.BasicAuth(login="api", password=API_KEY), data=data
    )
