# Copyright (C) 2022 Assistance.Chat contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import aiohttp

from .keys import get_notion_api_key

API_KEY = get_notion_api_key()


async def store_data_as_new_notion_page(parent_page_id, user_id, content):
    # TODO: Move the session object out
    async with aiohttp.ClientSession() as session:
        url = "https://api.notion.com/v1/pages"

        headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": f"Bearer {API_KEY}",
        }

        payload = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "Name": {"title": [{"text": {"content": user_id}}]},
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    },
                },
            ],
        }

        async with session.patch(url, json=payload, headers=headers) as resp:
            print(resp.status)
            json = await resp.json()

            try:
                print(json["message"])
            except KeyError:
                pass
