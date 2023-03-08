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

from assistance._types import Email
from assistance._config import (
    load_form_config,
    get_form_entries,
    get_complete_form_progression_keys,
    FormItem,
)
from assistance._forms.build import walk_and_build_form_fields
from assistance._forms.progression import get_task_for_current_stage

from .collect import collect_form_items


async def handle_enrolment_email(form_name: str, email: Email):
    user_email = email["user_email"]
    cfg = await load_form_config(form_name)
    form_entries = await get_form_entries(form_name, user_email)
    form_progression = await get_complete_form_progression_keys(form_name, user_email)

    remaining_form_fields_text = walk_and_build_form_fields(
        cfg["field"], ignore=set(form_entries.keys())
    )

    new_collected_items = await collect_form_items(
        email=email, remaining_form_fields_text=remaining_form_fields_text
    )
    new_form_entries = {
        key: FormItem(value=value, confirmed=False)
        for key, value in new_collected_items.items()
    }

    updated_form_entries = form_entries.copy()
    for key, item in new_form_entries.items():
        if key in updated_form_entries:
            if item["value"] == updated_form_entries[key]["value"]:
                continue

        updated_form_entries[key] = item

    # fields_that_need_validation = pa

    # TODO: Check for user confirmations of previously collected data

    # TODO: Collect items to validate with the user

    # TODO: Check whether the user is ready to for the next step in the
    # process

    # TODO: If the user isn't ready, simply respond to the email
    # answering their queries, as well as checking for any confirmation
    # required.

    # TODO: If the user is ready, get the next process and run it.
