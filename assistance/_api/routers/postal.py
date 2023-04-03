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

import json

import aiofiles
from fastapi import APIRouter, Request

from assistance._keys import get_mailgun_api_key
from assistance._paths import get_postal_path
from assistance._utilities import get_hash_digest

MAILGUN_API_KEY = get_mailgun_api_key()

router = APIRouter(prefix="/postal")


@router.post("")
async def receive_postal_webhook(request: Request):
    data = await request.json()

    await _store_postal_webhook(data)

    return {"message": "Queued. Thank you."}


async def _store_postal_webhook(data):
    try:
        webhook_to_store = json.dumps(data, indent=2)
    except TypeError:
        json_encodable_items = {}
        for key, item in data.items():
            try:
                json.dumps(item)
                json_encodable_items[key] = item
            except TypeError:
                json_encodable_items[key] = str(item)

        webhook_to_store = json.dumps(json_encodable_items, indent=2)

    hash_digest = get_hash_digest(webhook_to_store)
    postal_path = get_postal_path(hash_digest, create_parent=True)

    async with aiofiles.open(postal_path, mode="w") as f:
        await f.write(webhook_to_store)

    return hash_digest
