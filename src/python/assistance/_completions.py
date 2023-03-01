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
import pathlib
import time

import aiofiles
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

from assistance._logging import log_info

from ._paths import COMPLETIONS, get_completion_cache_path, get_hash_digest


async def get_completion_only(**kwargs) -> str:
    response = await _completion_with_back_off(**kwargs)

    return response["choices"][0]["message"]["content"].strip()  # type: ignore


async def _completion_with_back_off(**kwargs):
    scope: str = kwargs["scope"]
    del kwargs["scope"]

    assert "scope" not in kwargs

    kwargs_for_cache_hash = kwargs.copy()
    del kwargs_for_cache_hash["api_key"]

    completion_request = json.dumps(kwargs_for_cache_hash, indent=2, sort_keys=True)
    completion_request_hash = get_hash_digest(completion_request)
    completion_cache_path = get_completion_cache_path(
        completion_request_hash, create_parent=True
    )

    try:
        async with aiofiles.open(completion_cache_path, "r") as f:
            return json.loads(await f.read())
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    log_info(scope, f"New completion request: {completion_request}")

    query_timestamp = time.time_ns()

    response = await _run_completion(kwargs)

    asyncio.create_task(_store_cache(completion_cache_path, response))
    asyncio.create_task(_store_result(scope, kwargs, response, query_timestamp))

    return response


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(12))
async def _run_completion(kwargs):
    response = await _chat_completion_wrapper(**kwargs)

    return response


async def _chat_completion_wrapper(**kwargs):
    prompt = kwargs["prompt"]
    messages = [{"role": "user", "content": prompt}]

    del kwargs["prompt"]
    kwargs["messages"] = messages

    kwargs["model"] = kwargs["engine"]
    del kwargs["engine"]

    response = await openai.ChatCompletion.acreate(**kwargs)

    return response


async def _store_cache(completion_cache_path: pathlib.Path, response):
    async with aiofiles.open(completion_cache_path, "w") as f:
        await f.write(json.dumps(response, indent=2))


async def _store_result(user_email: str, kwargs, response, query_timestamp: int):
    usage_record_path = COMPLETIONS / user_email / f"{query_timestamp}.json"
    usage_record_path.parent.mkdir(parents=True, exist_ok=True)

    record = {"input": kwargs, "output": dict(response)}

    async with aiofiles.open(usage_record_path, "w") as f:
        await f.write(json.dumps(record, indent=2, sort_keys=True))
