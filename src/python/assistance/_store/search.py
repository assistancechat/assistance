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

from assistance._enums import SearchEngine
from assistance._paths import RECORDS

from .utilities import (
    create_record_directory_with_epoch,
    store_files_as_well_as_commit_hash,
)


async def store_search_result(
    record_grouping: str,
    username: str,
    search_engine: SearchEngine,
    search_query: str,
    search_api_result: dict,
    summary: str,
):
    record_directory = create_record_directory_with_epoch(
        RECORDS, [record_grouping, username, "search"]
    )

    data_to_save = {
        "search-engine.txt": search_engine.value,
        "search_query.txt": search_query,
        "search_api_result.json": json.dumps(search_api_result, indent=2),
        "summary.txt": summary,
    }

    asyncio.create_task(
        store_files_as_well_as_commit_hash(record_directory, data_to_save)
    )
