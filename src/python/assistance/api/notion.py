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


async def add_to_notion_page(password, page_id, content):
    # TODO: Move the session object out
    async with aiohttp.ClientSession() as session:
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"

        headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": f"Bearer {password}",
        }

        payload = {
            "children": [
                {
                    "object": "block",
                    "parent": {"type": "page_id", "page_id": page_id},
                    "has_children": False,
                    "archived": False,
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content,
                                },
                            }
                        ],
                        "color": "default",
                        "children": [],
                    },
                }
            ]
        }

        async with session.patch(url, json=payload, headers=headers) as resp:
            print(resp.status)
            json = await resp.json()

            try:
                print(json["message"])
            except KeyError:
                pass
