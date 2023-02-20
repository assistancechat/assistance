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
import time

import aiofiles
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

from ._paths import COMPLETIONS


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(12))
async def completion_with_back_off(**kwargs):
    user_email: str = kwargs["user_email"]
    del kwargs["user_email"]

    assert "user_email" not in kwargs

    query_timestamp = time.time_ns()
    response = await openai.Completion.acreate(**kwargs)
    logging.info(response)

    asyncio.create_task(_store_result(user_email, kwargs, response, query_timestamp))

    return response


async def _store_result(user_email: str, kwargs, response, query_timestamp: int):
    usage_record_path = COMPLETIONS / user_email / f"{query_timestamp}.json"
    usage_record_path.parent.mkdir(parents=True, exist_ok=True)

    record = {"input": kwargs, "output": dict(response)}

    async with aiofiles.open(usage_record_path, "w") as f:
        await f.write(json.dumps(record, indent=2, sort_keys=True))
