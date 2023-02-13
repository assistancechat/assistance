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
import json
from urllib.parse import urlparse

import aiohttp
from fastapi import APIRouter, Request
from pydantic import BaseModel

from assistance import _ctx
from assistance._config import ROOT_DOMAIN
from assistance._affiliate import decrypt_affiliate_tag
from assistance._keys import get_mailgun_api_key
from assistance._store.emails import store_contact_us_request

router = APIRouter(prefix="/forms")

EMAIL_SUBJECT = "{first_name} {last_name} filled out contact us form @ {origin_url}"
EMAIL_TEMPLATE = """{first_name} {last_name} has submitted a contact us form on {origin_url}.
Their email is {email} and their phone number is {phone_number}.

Agreed to terms and conditions: {agree_to_terms}

{referrer_details}

Their message is:
{message}

---

A reply to this email will be sent to {first_name} {last_name} using \
their email address {email}.
"""

REFERRER_TEMPLATE = """Their referrer tag is: {referrer_tag}
Which has the following content:
{referrer_tag_content}"""


MAILGUN_API_KEY = get_mailgun_api_key()


class ContactUsData(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    message: str
    agree_to_terms: bool
    referrer_tag: str | None = None


@router.post("/contact-us")
async def contact_us(data: ContactUsData, request: Request):
    origin_url = dict(request.scope["headers"]).get(b"referer", b"").decode()

    await _send_email(data, origin_url)


async def _send_email(data: ContactUsData, origin_url: str):
    url = f"https://api.eu.mailgun.net/v3/{ROOT_DOMAIN}/messages"

    if data.referrer_tag is None:
        referrer_details = "No referrer tag was provided."
    else:
        referrer_tag_content = decrypt_affiliate_tag(data.referrer_tag)

        referrer_details = REFERRER_TEMPLATE.format(
            referrer_tag=data.referrer_tag,
            referrer_tag_content=json.dumps(referrer_tag_content, indent=2),
        )

    mailgun_data = {
        "from": f"noreply@{ROOT_DOMAIN}",
        "to": "applications@globaltalent.work",
        "h:Reply-To": data.email,
        "subject": EMAIL_SUBJECT.format(
            origin_url=origin_url, first_name=data.first_name, last_name=data.last_name
        ),
        "text": EMAIL_TEMPLATE.format(
            origin_url=origin_url,
            referrer_details=referrer_details,
            **data.dict(),
        ),
    }

    mailgun_response = await _ctx.session.post(
        url=url,
        auth=aiohttp.BasicAuth(login="api", password=MAILGUN_API_KEY),
        data=mailgun_data,
    )

    record_grouping = urlparse(origin_url).netloc
    asyncio.create_task(
        store_contact_us_request(
            record_grouping=record_grouping,
            email_address=data.email,
            email_subject=mailgun_data["subject"],
            email_content=mailgun_data["text"],
            form_data=data.dict(),
            mailgun_data=mailgun_data,
            mailgun_response=mailgun_response,
        )
    )
