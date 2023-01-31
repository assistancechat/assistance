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

from assistance._paths import RECORDS

from .utilities import (
    create_record_directory_with_epoch,
    store_files_as_well_as_commit_hash,
)


async def store_prompt_transcript(
    record_grouping: str,
    client_email: str,
    model_kwargs: dict,
    prompt: str,
    response: str,
):
    record_directory = create_record_directory_with_epoch(
        RECORDS, [record_grouping, client_email, "transcripts"]
    )

    data_to_save = {
        "model-kwargs.json": json.dumps(model_kwargs, indent=2),
        "prompt.txt": prompt,
        "response.txt": response,
    }

    asyncio.create_task(
        store_files_as_well_as_commit_hash(record_directory, data_to_save)
    )
