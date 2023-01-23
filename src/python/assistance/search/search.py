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
import urllib.parse

from assistance import ctx
from assistance.keys import get_google_search_api_key
from assistance.store.search import store_search_result
from assistance.summary.with_query import summarise_urls_with_query_around_snippets

from .course_list import COURSE_LIST
from .ids import SEARCH_ENGINE_IDS, SearchEngine

API_KEY = get_google_search_api_key()

SEARCH_RESULTS_TO_USE = 3


async def alphacrucis_search(record_grouping: str, username: str, query: str):
    query = query + " alphacrucis"

    return await _search_with_summary(
        record_grouping=record_grouping,
        username=username,
        search_engine=SearchEngine.ALPHACRUCIS,
        query=query,
        added_pages=[COURSE_LIST],
    )


async def _search_with_summary(
    record_grouping: str,
    username: str,
    search_engine: SearchEngine,
    query: str,
    added_pages: list[str] | None = None,
):
    cx = SEARCH_ENGINE_IDS[search_engine]

    url_encoded_query = urllib.parse.quote(query)
    url = f"https://www.googleapis.com/customsearch/v1/siterestrict?key={API_KEY}&cx={cx}&q={url_encoded_query}"

    search_raw_results = await ctx.session.get(url=url)
    json_results = await search_raw_results.json()

    results_to_use = json_results["items"][0:SEARCH_RESULTS_TO_USE]

    links: list[str]
    snippets: list[str]
    try:
        links = [item["link"] for item in results_to_use]
        snippets = [item["snippet"] for item in results_to_use]
    except KeyError:
        links = []
        snippets = []

    cleaned_snippets_per_url = {}

    for link, snippet in zip(links, snippets):
        cleaned_snippet = [item.strip() for item in snippet.split("...")]
        cleaned_snippets_per_url[link] = [item for item in cleaned_snippet if item]

    logging.info(
        f"Cleaned Snippets per URL: {json.dumps(cleaned_snippets_per_url, indent=2)}"
    )

    if len(cleaned_snippets_per_url.keys()) + len(added_pages) == 0:
        summary = "No additional information found"

    else:
        summary = await summarise_urls_with_query_around_snippets(
            record_grouping=record_grouping,
            username=username,
            query=query,
            snippets_by_url=cleaned_snippets_per_url,
            added_pages=added_pages,
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
