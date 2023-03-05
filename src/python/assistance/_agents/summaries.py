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
import textwrap

from assistance import _ctx
from assistance._completions import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL
from assistance._logging import log_info
from assistance._utilities import (
    get_approximate_allowed_remaining_words,
    items_to_list_string,
)
from assistance._vendor.stackoverflow.web_scraping import scrape

MAX_NUMBER_OF_TEXT_SECTIONS = 20

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

NEWS_PROMPT = textwrap.dedent(
    """
        You are aiming to write a three paragraph summary of a section
        of information. The goal of this extraction is so as to allow
        someone else to fulfil the following tasks and goals about the
        information for their target audience:

        Their tasks:

        {tasks}

        Their goals:

        {goals}

        Their target audience:

        {target_audience}

        Your instructions:

        - If the text you are summarising is longer than three
          paragraphs, you should just provide the text itself instead.
        - Do not fulfil their tasks. Instead, ONLY provide a summary of
          the section of information itself in such a way to best equip
          someone else to fulfil the tasks and goals themselves.
        - If the information provided does not contain information that
          is relevant to the tasks or goals simply write NOT_RELEVANT
          instead of providing a summary. You MUST use exact formatting
          for NOT_RELEVANT, all caps with underscore.
        - ONLY provide information that is specifically within the
          information below. DO NOT utilise any of your outside
          knowledge to fill in any gaps.

        Section of information to summarise:

        {text}

        Your summary:
    """
).strip()

# EMAIL_PROMPT = textwrap.dedent(
#     """
#         You are aiming to write a three paragraph summary of a section
#         of information. The goal of this extraction is so as to allow
#         someone else to fulfil the following tasks and goals about the
#         information for their target audience:

#         Their tasks:

#         {tasks}

#         Their goals:

#         {goals}

#         Their target audience:

#         {target_audience}

#         Your instructions:

#         - If the text you are summarising is longer than three
#           paragraphs, you should just provide the text itself instead.
#         - Do not fulfil their tasks. Instead, ONLY provide a summary of
#           the section of information itself in such away to best equip
#           someone else to fulfil the tasks and goals themselves.
#         - If the information provided does not contain information that
#           is relevant to the tasks or goals simply write NOT_RELEVANT
#           instead of providing a summary.
#         - ONLY provide information that is specifically within the
#           information below. DO NOT utilise any of your outside
#           knowledge to fill in any gaps.

#         Section of information to summarise:

#         {text}

#         Your summary:
#     """
# ).strip()


WORD_COUNT_SCALING_BUFFER = 0.7
WORDS_OVERLAP = 40


async def summarise_news_article_url_with_tasks(
    scope: str,
    openai_api_key: str,
    tasks: list[str],
    goals: list[str],
    target_audience: str,
    url: str,
    use_google_cache=True,
):
    page_contents = await scrape(
        session=_ctx.session, url=url, use_google_cache=use_google_cache
    )

    summary = await summarise_text_with_tasks(
        scope=scope,
        openai_api_key=openai_api_key,
        tasks=tasks,
        goals=goals,
        target_audience=target_audience,
        text=page_contents,
    )

    log_info(scope, f"Summary of {url}: {summary}")

    return summary


async def summarise_text_with_tasks(
    scope: str,
    openai_api_key: str,
    tasks: list[str],
    goals: list[str],
    target_audience: str,
    text: str,
):
    prompt = NEWS_PROMPT.format(
        tasks=items_to_list_string(tasks),
        goals=items_to_list_string(goals),
        target_audience=target_audience,
        text="{text}",
    )

    log_info(scope, text)

    summary = await _summarise_piecewise(
        scope=scope,
        openai_api_key=openai_api_key,
        prompt=prompt,
        content_to_summarise=text,
    )

    return summary


async def _summarise_piecewise(
    scope: str,
    openai_api_key: str,
    prompt: str,
    content_to_summarise: str,
):
    split_page_contents_by_words = [
        item for item in content_to_summarise.split(None) if item
    ]

    remaining_words = get_approximate_allowed_remaining_words(
        prompt=prompt, max_tokens=MODEL_KWARGS["max_tokens"]
    )

    max_words_per_summary_section = int(
        remaining_words * WORD_COUNT_SCALING_BUFFER - WORDS_OVERLAP
    )

    all_text_sections = [
        " ".join(
            split_page_contents_by_words[
                i : i + max_words_per_summary_section + WORDS_OVERLAP
            ]
        )
        for i in range(
            0, len(split_page_contents_by_words), max_words_per_summary_section
        )
    ]

    if len(all_text_sections) > MAX_NUMBER_OF_TEXT_SECTIONS:
        log_info(scope, "Too many text sections, truncating...")

    text_sections = all_text_sections[:MAX_NUMBER_OF_TEXT_SECTIONS]

    if len(text_sections) == 0:
        return "NOT_RELEVANT"

    if len(text_sections) == 1:
        return await _evaluate_prompt(
            scope=scope,
            openai_api_key=openai_api_key,
            prompt=prompt,
            text=text_sections[0],
        )

    coroutines = []
    for text in text_sections:
        text = text.strip()

        if len(text) == 0:
            continue

        coroutines.append(
            _evaluate_prompt(
                scope=scope,
                openai_api_key=openai_api_key,
                prompt=prompt,
                text=text,
            )
        )

    summaries = await asyncio.gather(*coroutines)

    log_info(scope, f"All summaries: {_ctx.pprint.pformat(summaries)}")

    cleaned_summaries = [item for item in summaries if item != "NOT_RELEVANT"]
    combined_summaries = "\n\n".join(cleaned_summaries)

    summary = await _summarise_piecewise(
        scope=scope,
        openai_api_key=openai_api_key,
        prompt=prompt,
        content_to_summarise=combined_summaries,
    )

    return summary


async def _evaluate_prompt(
    scope: str,
    openai_api_key: str,
    prompt: str,
    text: str,
):
    response = await get_completion_only(
        scope=scope,
        prompt=prompt.format(text=text),
        api_key=openai_api_key,
        **MODEL_KWARGS,
    )

    return response
