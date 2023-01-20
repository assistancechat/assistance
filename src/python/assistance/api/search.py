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


import urllib.parse

from . import ctx
from .keys import get_google_search_api_key

API_KEY = get_google_search_api_key()


async def alphacrucis_search(query):
    cx = "350772bce9c914d64"
    return await _search_with_summary(cx=cx, query=query)


async def _search_with_summary(cx, query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict?key={API_KEY}&cx={cx}&q={encoded_query}"

    search_result = await ctx.session.get(url=url)

    return await search_result.json()
