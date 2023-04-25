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
import base64
import json
import pathlib
import re
import tomllib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable, Literal

import aiofiles
import aiosmtplib
import marko
import numpy as np
import pandas as pd

from assistance import _ctx
from assistance._keys import get_postal_api_key
from assistance._mailgun import send_email
from assistance._paths import EMAILS, MONOREPO, RECORDS, get_emails_path
from assistance._progression import (
    get_complete_progression_keys,
    get_current_stage_and_task,
    set_progression_key,
)
from assistance._utilities import EMAIL_PATTERN

POSTAL_API_KEY = get_postal_api_key()


async def campaign_workflow(
    cfg, name_lookup, email_list, dry_run=False, allowed_keys: None | set[str] = None
):
    coroutines = []
    for user_email_address in email_list:
        coroutines.append(
            _send_campaign_email(
                cfg=cfg,
                user_email_address=user_email_address,
                name_lookup=name_lookup,
                dry_run=dry_run,
                allowed_keys=allowed_keys,
            )
        )

    return await asyncio.gather(*coroutines)


async def _send_campaign_email(
    cfg, user_email_address, name_lookup, dry_run, allowed_keys: None | set[str]
):
    key, subject, body_template = await _get_email_template_for_user(
        cfg, user_email_address
    )

    if allowed_keys is not None:
        if key not in allowed_keys:
            return None, None

    if key is None or subject is None or body_template is None:
        return None, None

    if dry_run:
        return user_email_address, key

    mail_from = f"Alex Carpenter <{cfg['campaign_email_address']}>"

    await _create_and_send_email_with_signature(
        name_lookup=name_lookup,
        user_email_address=user_email_address,
        subject=subject,
        body_template=body_template,
        campaign_email_address=cfg["campaign_email_address"],
        signature_template=cfg["signature"],
        mail_from=mail_from,
    )

    await _update_progression_for_user(user_email_address, key)

    return user_email_address, key


async def _create_and_send_email_with_signature(
    name_lookup,
    user_email_address,
    subject,
    body_template: str,
    campaign_email_address,
    signature_template: str,
    mail_from,
):
    LOGO_PATH = MONOREPO / "images" / "logo.png"
    with open(LOGO_PATH, "rb") as f:
        image = MIMEImage(f.read())

    image.add_header("Content-ID", "logo")

    name = name_lookup[user_email_address]

    body_and_signature_template = body_template + "\n\n" + signature_template.strip()

    body = body_and_signature_template.format(
        name=name,
        campaign_email_address=campaign_email_address,
        user_email_address=user_email_address,
    )

    # Handles case where {name} is empty string
    body = body.replace(" ,", ",")

    message = MIMEMultipart("alternative")
    message["From"] = mail_from
    message["To"] = user_email_address
    message["Subject"] = subject

    plain_body = body
    html_body = marko.convert(plain_body)

    plain_text_message = MIMEText(plain_body, "plain", "utf-8")
    html_message = MIMEText(html_body, "html", "utf-8")
    message.attach(plain_text_message)
    message.attach(html_message)
    message.attach(image)

    b64_message = base64.b64encode(message.as_bytes()).decode()

    headers = {
        "Content-Type": "application/json",
        "X-Server-API-Key": POSTAL_API_KEY,
    }

    url = "https://postal.assistance.chat/api/v1/send/raw"

    postal_data = {
        "mail_from": mail_from,
        "rcpt_to": [user_email_address],
        "data": b64_message,
    }

    return await _ctx.session.post(
        url=url,
        headers=headers,
        data=json.dumps(postal_data),
    )


def _get_email_segments_and_name_lookup():
    formsite_export_path = RECORDS / "formsite" / "FormSiteExport20230404.csv"
    applications = pd.read_csv(formsite_export_path)

    incomplete_applications = _extract_emails(
        {
            email
            for email, status in zip(
                applications["Email Address"], applications["Status"]
            )
            if status != "Complete"
        }
    )
    started_application_emails = _extract_emails(
        set(applications["Username"])
        .union(applications["Email Address"], applications["Email"])
        .difference({np.NaN})
    )

    eoi_ads_leads_paths = (MONOREPO / "records" / "jims" / "emails" / "eoi").glob(
        "New Leads Ad_Leads_*.csv"
    )

    name_lookup = {}
    ads_leads_emails = set()

    for path in eoi_ads_leads_paths:
        eoi_ads_leads = pd.read_csv(
            path, encoding="utf-16", delimiter="\t", encoding_errors="replace"
        )
        for email, name in zip(eoi_ads_leads["email"], eoi_ads_leads["full_name"]):
            try:
                name_lookup[email.lower()] = name
            except AttributeError:
                pass

        ads_leads_emails.update(_extract_emails(eoi_ads_leads["email"]))

    eoi_second_path = (
        MONOREPO / "records" / "jims" / "emails" / "eoi" / "Contacts_2.csv"
    )
    eoi_second = pd.read_csv(
        eoi_second_path, encoding="utf-8", encoding_errors="ignore"
    )

    eoi_third_path = (
        MONOREPO / "records" / "jims" / "emails" / "eoi" / "SA Enquiries.xlsx"
    )
    eoi_third = pd.read_excel(eoi_third_path, header=None)

    all_eoi_emails = ads_leads_emails.union(
        _extract_emails(eoi_second["email address"]), _extract_emails(eoi_third[0])
    )

    unsubscribe_emails = _update_and_get_unsubscribes()

    bounced = MONOREPO / "records" / "jims" / "emails" / "bounced" / "first-run.csv"
    bounced_emails = _extract_emails(pd.read_csv(bounced)["email"])

    emails_to_remove = unsubscribe_emails.union(bounced_emails)

    for email, name in zip(eoi_third[0], eoi_third[1]):
        name_lookup[email.lower()] = name

    for email, first_name, last_name in zip(
        eoi_second["email address"], eoi_second["First Name"], eoi_second["Last Name"]
    ):
        if last_name == "*":
            name = first_name
        else:
            name = (first_name + " " + last_name).strip()
        name_lookup[email.lower()] = name

    for email, first_name, last_name in zip(
        applications["Email Address"],
        applications["First Name"],
        applications["Family Name"],
    ):
        if not isinstance(last_name, str):
            last_name = ""

        if not isinstance(first_name, str):
            first_name = ""

        name = (first_name + " " + last_name).strip()
        name_lookup[email.lower()] = name

    name_lookup["me@simonbiggs.net"] = "Simon Biggs"
    name_lookup["alex.carpenter@ac.edu.au"] = "Alex Carpenter"
    name_lookup["cameron.richardson@ac.edu.au"] = "Cameron Richardson"

    return (
        all_eoi_emails,
        emails_to_remove,
        started_application_emails,
        incomplete_applications,
        name_lookup,
    )


def _extract_emails(email_series: Iterable[str]):
    return {item.lower() for item in email_series if isinstance(item, str)}


def _update_and_get_unsubscribes():
    receiver = {}

    for path in EMAILS.glob("*/*/*.json"):
        with open(path) as f:
            try:
                receiver[path.stem] = json.load(f)["rcpt_to"]
            except:
                pass

    email_to_match = "pathways@jims.international"
    found_email_hashed = [
        key
        for key, item in receiver.items()
        if item is not None and email_to_match in item
    ]

    emails_to_unsubscribe = []

    for email_hash in found_email_hashed:
        path = get_emails_path(email_hash)

        with open(path) as f:
            email = json.load(f)

        try:
            if not "unsubscribe" in email["subject"].lower():
                continue
        except AttributeError:
            continue

        match = re.search(EMAIL_PATTERN, email["plain_body"])

        if match is None:
            emails_to_unsubscribe.append(email["mail_from"])
            continue

        email_address = match.group(0)
        emails_to_unsubscribe.append(email_address)

    unsubscribe_path = MONOREPO / "records" / "jims" / "emails" / "unsubscribe.csv"
    previous_unsubscribes = _extract_emails(
        pd.read_csv(unsubscribe_path, header=None)[0]
    )
    all_unsubscribes = previous_unsubscribes.union(emails_to_unsubscribe)
    unsubscribes_to_save = sorted([item.lower() for item in all_unsubscribes])

    pd.DataFrame(unsubscribes_to_save).to_csv(unsubscribe_path, header=None, index=None)  # type: ignore

    return all_unsubscribes


async def _get_email_template_for_user(cfg, user_email_address):
    complete_progression_keys = await get_complete_progression_keys(
        "campaign", "jims-ac", user_email_address
    )
    email_template = get_current_stage_and_task(
        cfg["emails"], complete_progression_keys
    )

    if email_template is None:
        return None, None, None

    subject = email_template["subject"].strip()
    body_template = email_template["body"].strip()

    return email_template["key"], subject, body_template


async def _update_progression_for_user(user_email_address: str, key: str):
    await set_progression_key("campaign", "jims-ac", user_email_address, key)
