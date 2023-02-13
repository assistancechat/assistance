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

from assistance._agents.email.reply import create_reply
from assistance._agents.email.custom import react_to_custom_agent_request
from assistance._agents.email.default import DEFAULT_TASKS
from assistance._agents.email.types import Email

from assistance._mailgun import send_email
from fastapi import APIRouter, Request


from assistance._keys import get_mailgun_api_key

MAILGUN_API_KEY = get_mailgun_api_key()

router = APIRouter(prefix="/email")


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
        email["subject"]
    except KeyError:
        email["subject"] = ""

    try:
        email["body-plain"]
    except KeyError:
        email["body-plain"] = ""

    if email["sender"] == "forwarding-noreply@google.com":
        await _respond_to_gmail_forward_request(email)

        return

    email["agent-name"] = email["recipient"].split("@")[0].lower()
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", email["from"])
    email["user-email"] = match.group(0).lower()

    if email["agent-name"] in DEFAULT_TASKS:
        task = DEFAULT_TASKS[email["agent-name"]][1]

        if isinstance(task, str):
            await react_to_custom_agent_request(email=email, prompt_task=task)

            return

        await task(email)

    path_to_new_prompt = PROMPTS_PATH / email["user-email"] / email["agent-name"]

    try:
        async with aiofiles.open(path_to_new_prompt) as f:
            prompt_task = await f.read()

    except FileNotFoundError:
        await _handle_no_custom_agent_created_yet_request(email)
        return

    await react_to_custom_agent_request(email=email, prompt_task=prompt_task)


async def _handle_no_custom_agent_created_yet_request(email: Email):
    response = (
        f"You have not created a custom agent for {email['agent-name']}@{ROOT_DOMAIN}. "
        f"Please send an email to create@{ROOT_DOMAIN} to create one.\n\n"
        f"When you send an email to create@{ROOT_DOMAIN} make sure to "
        f"mention that you want your agent to be called {email['agent-name']} "
        "as well as provide a reasonable prompt that makes sense for "
        "your agent."
    )

    subject, total_reply = create_reply(
        subject=email["subject"],
        body_plain=email["body-plain"],
        response=response,
        from_string=email["from"],
    )

    mailgun_data = {
        "from": f"{email['agent-name']}@{ROOT_DOMAIN}",
        "to": email["user-email"],
        "subject": subject,
        "text": total_reply,
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
