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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Literal

import aiofiles
import aiosmtplib
import marko

from assistance._config import ProgressionItem, get_file_based_mapping
from assistance._mailgun import send_email
from assistance._paths import CAMPAIGN_DATA, FORM_DATA


def get_current_stage_and_task(
    progression_cfg: list[ProgressionItem], complete_progression_keys: set[str]
) -> ProgressionItem | None:
    for item in progression_cfg:
        if item["key"] in complete_progression_keys:
            continue

        return item

    return None


ProgressionType = Literal["campaign", "form"]
PROGRESSION_TYPE_TO_ROOT: dict[ProgressionType, pathlib.Path] = {
    "campaign": CAMPAIGN_DATA,
    "form": FORM_DATA,
}


async def get_complete_progression_keys(
    progression_type: ProgressionType, progression_name: str, user_email: str
) -> set[str]:
    root = PROGRESSION_TYPE_TO_ROOT[progression_type]

    results = await get_file_based_mapping(
        root / progression_name / "progression", user_email, include_user=False
    )

    return results["empty_files"]


async def set_progression_key(
    progression_type: ProgressionType, progression_name: str, user_email: str, key: str
):
    root = PROGRESSION_TYPE_TO_ROOT[progression_type]

    path = root / progression_name / "progression" / user_email / key
    path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(path, "w"):
        pass


# @retry(
#     wait=wait_random_exponential(min=20, max=240),
#     stop=stop_after_attempt(12),
# )
async def send_campaign_email_with_progression(
    scope, campaign_cfg, name_lookup, user_email_address
):
    name = name_lookup[user_email_address]
    campaign_email_address = campaign_cfg["defaults"]["campaign_email_address"].strip()

    complete_progression_keys = await get_complete_progression_keys(
        "campaign", "jims-ac", user_email_address
    )
    email_template = get_current_stage_and_task(
        campaign_cfg["emails"], complete_progression_keys
    )

    if email_template is None:
        return

    subject = email_template["subject"].strip()
    body_template: str = (
        email_template["body"].strip()
        + "\n\n"
        + campaign_cfg["defaults"]["signature"].strip()
    )

    plain_body = body_template.format(
        name=name,
        user_email_address=user_email_address,
        campaign_email_address=campaign_email_address,
    )
    html_body = marko.convert(plain_body)

    postal_data = {
        "from": "Alex Carpenter <pathways@jims.international>",
        "to": [user_email_address],
        "subject": subject,
        "plain_body": plain_body,
        "html_body": html_body,
    }

    await send_email(scope, postal_data)

    await set_progression_key(
        "campaign", "jims-ac", user_email_address, email_template["key"]
    )

    return user_email_address, email_template["key"]
