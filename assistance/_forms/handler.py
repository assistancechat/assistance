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

import base64
import json
import pathlib
import tempfile
from typing import TypedDict

import aiofiles

from assistance._config import (
    FormItem,
    ProgressionItem,
    get_complete_form_progression_keys,
    get_form_entries,
    load_form_config,
    save_form_entries,
    set_progression_key,
)
from assistance._types import Email

from .build import walk_and_build_form_fields
from .collect import collect_form_items
from .confirmation import confirming_form_items
from .passport import get_fields_from_passport
from .progression import get_current_stage_and_task
from .response import write_and_send_email_response


async def handle_enrolment_email(form_name: str, email: Email):
    user_email = email["user_email"]

    cfg = await load_form_config(form_name)
    form_entries = await get_form_entries(form_name, user_email)

    fields_that_need_confirmation = set()
    for key, item in form_entries.items():
        if item["confirmed"]:
            continue

        fields_that_need_confirmation.add(key)

    if fields_that_need_confirmation:
        confirmation_form_fields_text, _ = walk_and_build_form_fields(
            cfg["field"], allow=fields_that_need_confirmation
        )

        error = None

        while True:
            try:
                form_fields_with_updated_confirmation = await confirming_form_items(
                    email=email,
                    confirmation_form_fields_text=confirmation_form_fields_text,
                    error=str(error),
                )
            except json.JSONDecodeError as e:
                error = e
                continue

            try:
                for key, item in form_fields_with_updated_confirmation.items():
                    if key not in form_entries:
                        continue

                    # We don't want to overwrite a previous confirmation
                    if (
                        form_entries[key]["value"] == item["value"]
                        and item["confirmed"]
                    ):
                        form_entries[key]["confirmed"] = True
            except KeyError as e:
                error = e
                continue

            break

    _, split_remaining_form_fields = walk_and_build_form_fields(
        cfg["field"], ignore=set(form_entries.keys())
    )

    new_collected_items = await collect_form_items(
        email=email, split_remaining_form_fields=split_remaining_form_fields
    )
    new_form_entries = {
        key: FormItem(value=value, confirmed=False)
        for key, value in new_collected_items.items()
    }

    for key, item in new_form_entries.items():
        if key in form_entries:
            if item["value"] == form_entries[key]["value"]:
                continue

        form_entries[key] = item

    progression = await _get_current_progression_item(
        cfg, form_name, user_email, form_entries
    )

    if progression["attachment_handler"]:
        handler = _ATTACHMENT_HANDLERS[progression["attachment_handler"]]
        extracted_form_values = await handler(email["attachments"])
        extracted_form_entries = {
            key: FormItem(value=value, confirmed=False)
            for key, value in extracted_form_values.items()
        }
        form_entries.update(extracted_form_entries)

    progression = await _get_current_progression_item(
        cfg, form_name, user_email, form_entries
    )

    fields_that_still_need_confirmation = set()
    for key, item in form_entries.items():
        if item["confirmed"]:
            continue

        fields_that_still_need_confirmation.add(key)

    confirmation_still_needed_text, _ = walk_and_build_form_fields(
        cfg["field"],
        allow=fields_that_still_need_confirmation,
        form_entries=form_entries,
        text_format="results",
    )

    updated_remaining_form_fields_text, _ = walk_and_build_form_fields(
        cfg["field"], ignore=set(form_entries.keys()), text_format="description-only"
    )

    await save_form_entries(form_name, user_email, form_entries)

    await write_and_send_email_response(
        email=email,
        form_name=form_name,
        current_step=progression["task"],
        remaining_form_fields=updated_remaining_form_fields_text,
        confirmation_still_needed=confirmation_still_needed_text,
    )

    if progression["always_run_at_least_once"]:
        await set_progression_key(form_name, user_email, progression["key"])


async def _get_current_progression_item(
    cfg, form_name, user_email, form_entries
) -> ProgressionItem:
    while True:
        completed_form_progression_items = await get_complete_form_progression_keys(
            form_name, user_email
        )
        progression = get_current_stage_and_task(
            cfg["progression"], completed_form_progression_items
        )

        if progression is None or progression["always_run_at_least_once"]:
            break

        if len(set(progression["fields_for_completion"]).difference(form_entries)) == 0:
            await set_progression_key(form_name, user_email, progression["key"])
            continue

        break

    if progression is None:
        progression = cfg["progression"][-1]

    return progression


class Attachment(TypedDict):
    content_type: str
    data: str
    filename: str
    size: int


async def _extract_passport_details_as_field_items(attachments: list[Attachment]):
    passport_details = await _extract_passport_details(attachments)

    assert passport_details is not None

    return {
        "personal.first-name": passport_details["first_name"],
        "personal.middle-names": passport_details["middle_names"],
        "personal.family-name": passport_details["family_name"],
        "personal.date-of-birth": passport_details["date_of_birth"],
        "personal.nationality": passport_details["nationality"],
        "personal.passport-number": passport_details["passport_number"],
        "personal.passport-expiry-date": passport_details["passport_expiry_date"],
    }


async def _extract_passport_details(attachments: list[Attachment]):
    for attachment in attachments:
        img_data = base64.b64decode(attachment["data"].encode())

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dir = pathlib.Path(tmp_dir_name)
            path = dir / attachment["filename"]
            async with aiofiles.open(path, "wb") as f:
                await f.write(img_data)

            try:
                passport_details = get_fields_from_passport(str(path))

            # TODO: Improve this
            except Exception as e:
                print(e)
                continue
            else:
                return passport_details


_ATTACHMENT_HANDLERS = {
    "extract_passport_details": _extract_passport_details_as_field_items,
}
