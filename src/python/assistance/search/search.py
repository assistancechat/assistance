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
import logging
import urllib.parse

from assistance import ctx
from assistance.keys import get_google_search_api_key
from assistance.store.search import store_search_result
from assistance.summary.with_query import summarise_urls_with_query

from .ids import SEARCH_ENGINE_IDS, SearchEngine

API_KEY = get_google_search_api_key()


async def alphacrucis_search(record_grouping: str, username: str, query: str):
    query = query.lower().replace("alphacrusis", "") + " alphacrusis"

    return await _search_with_summary(
        record_grouping=record_grouping,
        username=username,
        search_engine=SearchEngine.ALPHACRUCIS,
        query=query,
    )


async def _search_with_summary(
    record_grouping: str, username: str, search_engine: SearchEngine, query: str
):
    cx = SEARCH_ENGINE_IDS[search_engine]

    url_encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict?key={API_KEY}&cx={cx}&q={url_encoded_query}"

    search_raw_results = await ctx.session.get(url=url)
    json_results = await search_raw_results.json()

    links: list[str]
    try:
        links = [item["link"] for item in json_results["items"]]
    except KeyError:
        links = []

    logging.info(f"Search Links: {links}")

    if len(links) == 0:
        summary = "No additional information found"

    else:
        links_to_use = links[0:10]
        logging.info(links_to_use)

        summary = await summarise_urls_with_query(
            record_grouping=record_grouping,
            username=username,
            query=query,
            urls=links_to_use,
        )

    asyncio.create_task(
        store_search_result(
            record_grouping=record_grouping,
            username=username,
            search_engine=search_engine,
            search_query=query,
            search_api_result=json_results,
            summary=summary,
        )
    )

    logging.info(f"Search Summary: {summary}")

    return summary
