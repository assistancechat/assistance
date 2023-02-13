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

import aiofiles
import re
import asyncio
from typing import TypedDict
from urllib.parse import parse_qs
import json
import logging

from assistance import _ctx
from assistance._config import ROOT_DOMAIN
from assistance._paths import PROMPTS as PROMPTS_PATH

from assistance._agents.email.create import react_to_create_domain
from assistance._agents.email.custom import react_to_custom_agent_request
from assistance._agents.email.default import DEFAULT_TASKS
from assistance._mailgun import send_email
from fastapi import APIRouter, Request


from assistance._keys import get_mailgun_api_key

MAILGUN_API_KEY = get_mailgun_api_key()

router = APIRouter(prefix="/email")

Email = TypedDict(
    "Email",
    {
        "recipient": str,
        "sender": str,
        "from": str,
        "stripped-text": str,
        "subject": str,
        "timestamp": str,
        "body-plain": str,
    },
    total=False,
)


@router.post("")
async def email(request: Request):
    encoded_body = await request.body()
    body = encoded_body.decode("utf-8")

    details = parse_qs(body)

    flatten_list_items = {}
    for key, item in details.items():
        if len(item) != 1:
            flatten_list_items[key] = item
            continue

        flatten_list_items[key] = item[0]

    email = Email(flatten_list_items)
    logging.info(json.dumps(email, indent=2))

    await _react_to_email(email)

    return "Success"


async def _react_to_email(email: Email):
    try:
        subject = email["subject"]
    except KeyError:
        subject = ""

    try:
        body_plain = email["body-plain"]
    except KeyError:
        body_plain = ""

    from_string = email["from"]

    if email["sender"] == "forwarding-noreply@google.com":
        await _respond_to_gmail_forward_request(email)

        return

    agent_name = email["recipient"].split("@")[0].lower()

    if email["recipient"] == f"create@{ROOT_DOMAIN}":
        await react_to_create_domain(
            from_string=from_string,
            subject=subject,
            body_plain=body_plain,
        )

        return

    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", from_string)
    user_email_address = match.group(0)

    if agent_name in DEFAULT_TASKS:
        await react_to_custom_agent_request(
            from_string=from_string,
            subject=subject,
            user_email_address=user_email_address,
            body_plain=body_plain,
            agent_name=agent_name,
            prompt_task=DEFAULT_TASKS[agent_name][1],
        )

        return

    path_to_new_prompt = PROMPTS_PATH / user_email_address / agent_name

    try:
        async with aiofiles.open(path_to_new_prompt) as f:
            prompt_task = await f.read()

    except FileNotFoundError:
        await _handle_no_custom_agent_created_yet_request(
            agent_name=agent_name,
            user_email_address=user_email_address,
            subject=subject,
        )
        return

    await react_to_custom_agent_request(
        from_string=from_string,
        subject=subject,
        user_email_address=user_email_address,
        body_plain=body_plain,
        agent_name=agent_name,
        prompt_task=prompt_task,
    )


async def _handle_no_custom_agent_created_yet_request(
    agent_name: str, user_email_address: str, subject: str
):
    response = (
        f"You have not created a custom agent for {agent_name}@{ROOT_DOMAIN}. "
        f"Please send an email to create@{ROOT_DOMAIN} to create one.\n\n"
        f"When you send an email to create@{ROOT_DOMAIN} make sure to "
        f"mention that you want your agent to be called {agent_name} "
        "as well as provide a reasonable prompt that makes sense for "
        "your agent."
    )

    if not subject.startswith("Re:"):
        subject = f"Re: {subject}"

    mailgun_data = {
        "from": f"{agent_name}@{ROOT_DOMAIN}",
        "to": user_email_address,
        "subject": subject,
        "text": response,
    }

    asyncio.create_task(send_email(mailgun_data))


VERIFICATION_TOKEN_BASE = "https://mail.google.com/mail/vf-"
VERIFICATION_TOKEN_BASE_ALTERNATIVE = "https://mail-settings.google.com/mail/vf-"


async def _respond_to_gmail_forward_request(email: Email):
    forwarding_email = email["recipient"]

    found_token = None

    for item in email["stripped-text"].splitlines():
        logging.info(item)

        for option in [VERIFICATION_TOKEN_BASE, VERIFICATION_TOKEN_BASE_ALTERNATIVE]:
            if item.startswith(option):
                found_token = item.removeprefix(option)
                break

    assert found_token is not None

    asyncio.create_task(_post_gmail_forwarding_verification(found_token))

    user_email = email["stripped-text"].split(" ")[0]
    logging.info(f"User email: {user_email}")

    mailgun_data = {
        "from": forwarding_email,
        "to": user_email,
        "subject": "Email forwarding approved",
        "text": (
            "Hi!\n",
            f"We've approved your ability to be able to forward emails through to {forwarding_email}.",
        ),
    }

    asyncio.create_task(send_email(mailgun_data))


async def _post_gmail_forwarding_verification(verification_token):
    forwarding_verification_post_url = f"{VERIFICATION_TOKEN_BASE}{verification_token}"
    logging.info(forwarding_verification_post_url)

    post_response = await _ctx.session.post(url=forwarding_verification_post_url)

    logging.info(await post_response.read())
