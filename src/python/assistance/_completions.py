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
import functools
import json
import logging
import time

import aiofiles
import openai
from async_lru import alru_cache
from tenacity import retry, stop_after_attempt, wait_random_exponential

from ._paths import COMPLETIONS


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(12))
async def completion_with_back_off(**kwargs):
    llm_usage_record_key: str = kwargs["llm_usage_record_key"]
    del kwargs["llm_usage_record_key"]

    assert "llm_usage_record_key" not in kwargs

    query_timestamp, response = await _run_completion_with_lru_cache(kwargs)

    # Timestamp will be from when it was called the first time through.
    asyncio.create_task(
        _store_result(llm_usage_record_key, kwargs, response, query_timestamp)
    )

    return response


@alru_cache(maxsize=1024)
async def _run_completion_with_lru_cache(kwargs):
    query_timestamp = time.time_ns()

    logging.info(f"New completion request: {kwargs}")

    response = await openai.Completion.acreate(**kwargs)
    logging.info(response)

    return query_timestamp, response


async def _store_result(user_email: str, kwargs, response, query_timestamp: int):
    usage_record_path = COMPLETIONS / user_email / f"{query_timestamp}.json"
    usage_record_path.parent.mkdir(parents=True, exist_ok=True)

    record = {"input": kwargs, "output": dict(response)}

    async with aiofiles.open(usage_record_path, "w") as f:
        await f.write(json.dumps(record, indent=2, sort_keys=True))
