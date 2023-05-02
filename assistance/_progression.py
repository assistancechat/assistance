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

import time
import pathlib
from typing import Literal

import aiofiles

from assistance._config import ProgressionItem, get_file_based_mapping
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

    return set(results.keys())


async def set_progression_key(
    progression_type: ProgressionType, progression_name: str, user_email: str, key: str
):
    root = PROGRESSION_TYPE_TO_ROOT[progression_type]

    path = root / progression_name / "progression" / user_email / key

    if path.exists():
        raise ValueError("Tried to set a progression key that already exists")

    path.parent.mkdir(parents=True, exist_ok=True)

    progression_file_contents = str(time.time())

    async with aiofiles.open(path, "w") as f:
        await f.write(progression_file_contents)
