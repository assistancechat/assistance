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
import logging
import re

import aiofiles
from fastapi import APIRouter, Request

from assistance import _ctx
from assistance._agents.email.custom import react_to_custom_agent_request
from assistance._agents.email.default import DEFAULT_TASKS
from assistance._agents.email.reply import create_reply
from assistance._agents.email.restricted import RESTRICTED_TASKS
from assistance._agents.email.types import Email
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_mailgun_api_key
from assistance._mailgun import send_email
from assistance._paths import (
    NEW_EMAILS,
    get_agent_mappings,
    get_emails_path,
    get_hash_digest,
    get_user_details,
    get_user_from_email,
)

MAILGUN_API_KEY = get_mailgun_api_key()

router = APIRouter(prefix="/email")


@router.post("")
async def email(request: Request):
    email = Email(await request.form())

    logging.info(_ctx.pp.pformat(email))

    hash_digest = await _store_email(email)

    asyncio.create_task(_handle_new_email(hash_digest, email))

    return {"message": "Queued. Thank you."}


# TODO: Handle attachments
async def _store_email(email: Email):
    try:
        email_to_store = json.dumps(email, indent=2)
    except json.decoder.JSONDecodeError:
        json_encodable_items = {}
        for key, item in email.items():
            try:
                json.dumps(item)
                json_encodable_items[key] = item
            except json.decoder.JSONDecodeError:
                json_encodable_items[key] = str(item)

        email_to_store = json.dumps(json_encodable_items, indent=2)

    hash_digest = get_hash_digest(email_to_store)
    emails_path = get_emails_path(hash_digest, create_parent=True)

    async with aiofiles.open(emails_path, "w") as f:
        await f.write(email_to_store)

    pipeline_path = _get_new_email_pipeline_path(hash_digest)
    async with aiofiles.open(pipeline_path, "w") as f:
        pass

    return hash_digest


def _get_new_email_pipeline_path(hash_digest: str):
    return NEW_EMAILS / hash_digest


async def _handle_new_email(hash_digest: str, email: Email):
    """React to the new email, and once it completes without error, delete the pipeline file."""

    email = await _initial_parsing(email)
    await _react_to_email(email)

    pipeline_path = _get_new_email_pipeline_path(hash_digest)
    pipeline_path.unlink()


async def _react_to_email(email: Email):
    if email["from"] == email["recipient"]:
        logging.info(
            "Email is from the same address as the recipient. "
            "Breaking loop. Doing nothing."
        )
        return

    if email["sender"] == "forwarding-noreply@google.com":
        await _respond_to_gmail_forward_request(email)

        return

    user_details, agent_mappings = await _get_user_details_and_mappings(email)

    try:
        mapped_agent = agent_mappings[email["agent-name"]]
    except KeyError:
        pass
    else:
        await RESTRICTED_TASKS[mapped_agent](user_details=user_details, email=email)

        return

    try:
        task = DEFAULT_TASKS[email["agent-name"]][1]
    except KeyError:
        pass
    else:
        if isinstance(task, str):
            await react_to_custom_agent_request(email=email, prompt_task=task)
        else:
            await task(email)

        return

    await _fallback_email_handler(user_details=user_details, email=email)
    return


async def _get_user_details_and_mappings(email: Email):
    try:
        user = await get_user_from_email(email["user-email"])
    except ValueError:
        first_name = email["from"].split(" ")[0].capitalize()
        user_details = {"first_name": first_name}
        agent_mappings = {}

        return user_details, agent_mappings

    user_details = await get_user_details(user)
    agent_mappings = await get_agent_mappings(user)

    return user_details, agent_mappings


async def _fallback_email_handler(user_details: dict, email: Email):
    response = (
        f"Hi {user_details['first_name']},\n\n"
        "This particular Assistance.Chat agent has not yet been implemented "
        "for your user account.\n\n"
        "I have included Simon, the developer of this software into this email, "
        "hopefully he might be able to help you on where to go from here.\n\n"
        "Kind regards,\n"
        "Assistance.Chat"
    )

    subject, total_reply = create_reply(
        original_email=email,
        response=response,
    )

    mailgun_data = {
        "from": f"{email['agent-name']}@{ROOT_DOMAIN}",
        "to": email["user-email"],
        "cc": "me@simonbiggs.net",
        "subject": subject,
        "text": total_reply,
    }

    await send_email(mailgun_data)


async def _initial_parsing(email: Email):
    try:
        email["subject"]
    except KeyError:
        email["subject"] = ""

    try:
        email["body-plain"]
    except KeyError:
        email["body-plain"] = ""

    email["agent-name"] = email["recipient"].split("@")[0].lower()

    try:
        x_forwarded_for = email["X-Forwarded-For"]
        email["user-email"] = x_forwarded_for.split(" ")[0].lower()

        assert _get_cleaned_email(email["sender"]) == email["user-email"]

    except KeyError:
        email["user-email"] = _get_cleaned_email(email["from"])

    return email


EMAIL_PATTERN = re.compile(
    r"(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))"
)


def _get_cleaned_email(email_string: str):
    match = re.search(EMAIL_PATTERN, email_string)

    sender_domain = match.group(5)
    sender_username = match.group(1)
    cleaned_username = sender_username.split("+")[0]

    return f"{cleaned_username}@{sender_domain}".lower()


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

    await _post_gmail_forwarding_verification(found_token)

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

    await send_email(mailgun_data)


async def _post_gmail_forwarding_verification(verification_token):
    forwarding_verification_post_url = f"{VERIFICATION_TOKEN_BASE}{verification_token}"
    logging.info(forwarding_verification_post_url)

    post_response = await _ctx.session.post(url=forwarding_verification_post_url)

    logging.info(await post_response.read())
