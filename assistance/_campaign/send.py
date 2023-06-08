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

import logging
import time
from collections import defaultdict
import asyncio
import base64
import json
import re
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Iterable


import marko
import numpy as np
import pandas as pd

from assistance import _ctx
from assistance._keys import get_postal_api_key
from assistance._paths import (
    EMAILS,
    MONOREPO,
    RECORDS,
    get_emails_path,
    CONTACT_FORM,
    CAMPAIGN_DATA,
)
from assistance._progression import (
    get_complete_progression_keys,
    get_current_stage_and_task,
    set_progression_key,
)
from assistance._utilities import EMAIL_PATTERN


POSTAL_API_KEY = get_postal_api_key()
THIRTY_SIX_HOURS = 36 * 60 * 60
TWENTY_FOUR_HOURS = 24 * 60 * 60


async def campaign_workflow(
    cfg,
    name_lookup,
    email_list: set[str],
    dry_run=False,
    allowed_keys: None | set[str] = None,
    skip_recently_emailed=True,
):
    if skip_recently_emailed:
        recently_emailed = await _emails_recently_sent(tolerance=THIRTY_SIX_HOURS)
        email_list -= recently_emailed

    semaphore = asyncio.Semaphore(50)

    coroutines = []
    for user_email_address in email_list:
        coroutines.append(
            _send_campaign_email(
                cfg=cfg,
                user_email_address=user_email_address,
                name_lookup=name_lookup,
                dry_run=dry_run,
                allowed_keys=allowed_keys,
                semaphore=semaphore,
            )
        )

    results = await asyncio.gather(*coroutines)

    filtered_results = [item for item in results if item[0] is not None]
    return filtered_results


async def _send_campaign_email(
    cfg,
    user_email_address,
    name_lookup,
    dry_run,
    allowed_keys: None | set[str],
    semaphore: asyncio.Semaphore,
):
    async with semaphore:
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


async def get_email_segments_and_name_lookup():
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

        try:
            for email, name in zip(eoi_ads_leads["email"], eoi_ads_leads["full_name"]):
                try:
                    name_lookup[email.lower()] = name
                except AttributeError:
                    pass
        except KeyError:
            logging.warning(f"Had key error, columns are {eoi_ads_leads.columns}")
            raise

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

    contact_form_entries = _get_contact_form_eois()
    contact_form_emails = _extract_emails(
        {entry["email"] for entry in contact_form_entries}
    )

    all_eoi_emails = ads_leads_emails.union(
        _extract_emails(eoi_second["email address"]),
        _extract_emails(eoi_third[0]),
        contact_form_emails,
    )

    unsubscribe_emails = _update_and_get_unsubscribes()

    bounced = MONOREPO / "records" / "jims" / "emails" / "bounced" / "first-run.csv"
    bounced_emails = _extract_emails(pd.read_csv(bounced)["email"])

    emails_to_remove = unsubscribe_emails.union(bounced_emails)

    for email, name in zip(eoi_third[0], eoi_third[1]):
        try:
            name_lookup[email.lower()] = name
        except AttributeError:
            pass

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

    for entry in contact_form_entries:
        name_lookup[
            entry["email"].lower()
        ] = f'{entry["first-name"]} {entry["last-name"]}'

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


def _get_contact_form_eois():
    form_entries = []

    for path in CONTACT_FORM.glob("*/*/*.json"):
        with open(path) as f:
            form_entries.append(json.load(f))

    return form_entries


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


async def _emails_recently_sent(tolerance=4000):
    last_touched = await _get_last_touched()

    now = time.time()
    diff = {key: now - item for key, item in last_touched.items()}

    recently_emailed = {key for key, item in diff.items() if item < tolerance}

    return recently_emailed


async def _get_last_touched():
    last_touched: dict[str, float] = defaultdict(lambda: 0.0)
    progression_record = (CAMPAIGN_DATA / "jims-ac" / "progression").glob("*/*")

    for record in progression_record:
        last_touched[record.parent.name] = max(
            last_touched[record.parent.name], record.stat().st_mtime
        )

    return last_touched
