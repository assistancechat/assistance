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
import math
import statistics
import textwrap

import openai
from thefuzz import process as fuzz_process

from assistance._vendor.stackoverflow.web_scraping import scrape

from .summary import _ctx

MAX_TEXT_SECTIONS = 10
MIN_TEXT_LENGTH = 5
MAX_TEXT_LENGTH = 200

# The amount of words to include either side of a Google search snippet
WORDS_CONTEXT = 100
MAX_WORDS_IN_CONTEXT = WORDS_CONTEXT * 2 + 1

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 1,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

PROMPT = textwrap.dedent(
    """
        Collate summaries that might be relevant to the query
        below by utilising the provided text. If none of the
        information is relevant to the query respond only
        with the statement NOT_RELEVANT.

        Only include information that is explicitly found within the
        text.

        Query:
        {query}

        Text:
        {text}

        Collated Summaries:
    """
).strip()


async def summarise_piecewise_with_query(
    record_grouping: str, username: str, query: str, text_sections: list[str]
):
    if len(text_sections) == 0:
        return "NOT_RELEVANT"

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

    cleaned_summaries = [item for item in summaries if item != "NOT_RELEVANT"]
    combined_summaries = "\n\n".join(cleaned_summaries)

    summary = await summarise_with_query(
        record_grouping=record_grouping,
        username=username,
        query=query,
        text=combined_summaries,
    )

    return summary


async def summarise_urls_with_query_around_snippets(
    record_grouping: str,
    username: str,
    query: str,
    snippets_by_url: dict[str, list[str]],
    added_pages: list[str] | None = None,
):
    urls = list(snippets_by_url.keys())
    total_number_of_pages = len(urls) + len(added_pages)

    if total_number_of_pages == 0:
        return "NOT_RELEVANT"

    coroutines = []
    for page in added_pages:
        coroutines.append(
            summarise_with_query(
                record_grouping=record_grouping,
                username=username,
                query=query,
                text=page,
            )
        )

    for url, snippets in snippets_by_url.items():
        coroutines.append(
            summarise_url_with_query_around_snippets(
                record_grouping=record_grouping,
                username=username,
                query=query,
                url=url,
                snippets=snippets,
            )
        )

    summaries = await asyncio.gather(*coroutines)

    cleaned_summaries = [item for item in summaries if item != "NOT_RELEVANT"]
    combined_summaries = "\n\n".join(cleaned_summaries)

    summary = await summarise_with_query(
        record_grouping=record_grouping,
        username=username,
        query=query,
        text=combined_summaries,
    )

    return summary


def _pull_only_relevant(split_page_contents_by_words: str, snippets: str):
    page_snippets_with_context = []

    # Have extracted snippets scan the page skipping 10 words at a time
    word_skip = 10

    for i in range(0, len(split_page_contents_by_words), word_skip):
        context_min = max(0, i - WORDS_CONTEXT)
        context_max = i + WORDS_CONTEXT

        page_snippets_with_context.append(
            " ".join(split_page_contents_by_words[context_min:context_max])
        )

    fuzz_limit = int(math.ceil(MAX_WORDS_IN_CONTEXT) / word_skip)
    snippets_to_summarise = []
    for snippet in snippets:
        selections_found = fuzz_process.extractBests(
            snippet, page_snippets_with_context, limit=fuzz_limit
        )

        # This is required so that the snippet used has context either
        # side of the snippet itself
        selections = [item[0] for item in selections_found]
        indices = [page_snippets_with_context.index(item) for item in selections]
        median_index = int(round(statistics.median(indices)))

        snippet_with_context = page_snippets_with_context[median_index]

        snippets_to_summarise.append(snippet)
        snippets_to_summarise.append(snippet_with_context)

    extracted_snippets_with_context = "\n\n".join(snippets_to_summarise)

    return extracted_snippets_with_context


async def summarise_url_with_query_around_snippets(
    record_grouping: str, username: str, query: str, url: str, snippets: list[str]
):
    page_contents = await scrape(session=_ctx.session, url=url)

    split_page_contents_by_words = [item for item in page_contents.split(None) if item]

    if len(split_page_contents_by_words) < MAX_WORDS_IN_CONTEXT:
        to_summarise = (
            "\n\n".join(snippets) + "\n\n" + " ".join(split_page_contents_by_words)
        )
    else:
        to_summarise = _pull_only_relevant(split_page_contents_by_words, snippets)

    logging.info(f"URL: {url}\nTo Summarise: {to_summarise}")

    summary = await summarise_with_query(
        record_grouping=record_grouping,
        username=username,
        query=query,
        text=to_summarise,
    )

    logging.info(f"Summary of {url}: {summary}")

    return summary


async def summarise_with_query(
    record_grouping: str, username: str, query: str, text: str
):
    prompt = PROMPT.format(query=query, text=text)

    completions = await openai.Completion.acreate(prompt=prompt, **MODEL_KWARGS)
    response: str = completions.choices[0].text.strip()

    return response
