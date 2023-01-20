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
import textwrap

import openai

from assistance import ctx
from assistance.vendor.stackoverflow.web_scraping import scrape

MAX_TEXT_SECTIONS = 10
MIN_TEXT_LENGTH = 5
MAX_TEXT_LENGTH = 200

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 1,
    "temperature": 0.0,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

PROMPT = textwrap.dedent(
    """
        Answer the query below utilising the provided information.
        If the information is not relevant to the query respond with
        "Not relevant".

        Query:
        {query}

        Information:
        {text}

        Answer:
    """
).strip()


async def summarise_piecewise_with_query(
    record_grouping: str, username: str, query: str, text_sections: list[str]
):
    if len(text_sections) == 0:
        return "Not relevant"

    if len(text_sections) == 1:
        return await summarise_with_query(
            record_grouping=record_grouping,
            username=username,
            query=query,
            text=text_sections[0],
        )

    cleaned_text_sections = []
    for text in text_sections:
        text = text.strip()

        if len(text) < MIN_TEXT_LENGTH:
            continue

        cleaned_text_sections.append(text[0:MAX_TEXT_LENGTH])

    limited_text_sections = cleaned_text_sections[0:MAX_TEXT_SECTIONS]

    coroutines = []
    for text in limited_text_sections:
        text = text.strip()

        if len(text) == 0:
            continue

        coroutines.append(
            summarise_with_query(
                record_grouping=record_grouping,
                username=username,
                query=query,
                text=text,
            )
        )

    summaries = await asyncio.gather(*coroutines)

    cleaned_summaries = [item for item in summaries if item != "Not relevant"]
    combined_summaries = "\n\n".join(cleaned_summaries)

    summary = await summarise_with_query(
        record_grouping=record_grouping,
        username=username,
        query=query,
        text=combined_summaries,
    )

    return summary


async def summarise_urls_with_query(
    record_grouping: str, username: str, query: str, urls: list[str]
):
    if len(urls) == 0:
        return "Not relevant"

    if len(urls) == 1:
        return await summarise_url_with_query(
            record_grouping=record_grouping,
            username=username,
            query=query,
            url=urls[0],
        )

    coroutines = []

    for url in urls:
        coroutines.append(
            summarise_url_with_query(
                record_grouping=record_grouping,
                username=username,
                query=query,
                url=url,
            )
        )

    summaries = await asyncio.gather(*coroutines)

    cleaned_summaries = [item for item in summaries if item != "Not relevant"]
    combined_summaries = "\n\n".join(cleaned_summaries)

    summary = await summarise_with_query(
        record_grouping=record_grouping,
        username=username,
        query=query,
        text=combined_summaries,
    )

    return summary


async def summarise_url_with_query(
    record_grouping: str, username: str, query: str, url: str
):
    page_contents = await scrape(session=ctx.session, url=url)

    split_page_contents = [item for item in page_contents.split(" ") if item]
    word_limited = split_page_contents[0:200]

    word_limited_contents = " ".join(word_limited)

    summary = await summarise_with_query(
        record_grouping=record_grouping,
        username=username,
        query=query,
        text=word_limited_contents,
    )

    return summary


async def summarise_with_query(
    record_grouping: str, username: str, query: str, text: str
):
    prompt = PROMPT.format(query=query, text=text)

    completions = await openai.Completion.acreate(prompt=prompt, **MODEL_KWARGS)
    response: str = completions.choices[0].text.strip()

    return response
