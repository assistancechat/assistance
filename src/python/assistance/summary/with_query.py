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

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 2,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

PROMPT = textwrap.dedent(
    """
        Summarise the following text in light of the following query.
        If the text is not relevant to the query respond with "Not relevant"

        Query:
        {query}

        Text:
        {text}

        Summary:
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

    coroutines = []

    for text in text_sections:
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

    summaries = asyncio.gather(coroutines)

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
    split_page_contents = page_contents.split("\n\n")

    summary = await summarise_piecewise_with_query(
        record_grouping=record_grouping,
        username=username,
        query=query,
        text_sections=split_page_contents,
    )

    return summary


async def summarise_with_query(
    record_grouping: str, username: str, query: str, text: str
):
    prompt = PROMPT.format(query=query, text=text)

    completions = await openai.Completion.acreate(prompt=prompt, **MODEL_KWARGS)
    response: str = completions.choices[0].text.strip()

    return response
