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
from assistance._completions import completion_with_back_off
from assistance._vendor.stackoverflow.web_scraping import scrape

MAX_NUMBER_OF_TEXT_SECTIONS = 20

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 512,
    "best_of": 1,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

# ~4097 * 0.75
APPROXIMATE_ALLOWED_WORDS_IN_PROMPT = 3000

PROMPT = textwrap.dedent(
    """
        You are aiming to summarise a section of information in order to
        extract the key information that will allow someone else to
        answer the following questions:

        {questions}

        Do not answer the questions themselves. Instead, ONLY provide a
        summary of the section of information itself in such away to
        best equip someone else to answer the questions.

        Section of information to summarise:

        {text}

        Your summary:
    """
).strip()

LEN_OF_PROMPT = len(PROMPT.format(questions="", text=""))
REMAINING_WORDS_IN_PROMPT = (
    APPROXIMATE_ALLOWED_WORDS_IN_PROMPT
    - LEN_OF_PROMPT
    - MODEL_KWARGS["max_tokens"] * 0.75
)

WORD_COUNT_SCALING_BUFFER = 0.8
WORDS_OVERLAP = 20


async def summarise_url_with_questions(
    openai_api_key: str,
    questions: str,
    url: str,
):
    page_contents = await scrape(session=_ctx.session, url=url)

    split_page_contents_by_words = [item for item in page_contents.split(None) if item]

    remaining_words = REMAINING_WORDS_IN_PROMPT - len(questions)
    max_words_per_summary_section = (
        remaining_words * WORD_COUNT_SCALING_BUFFER - WORDS_OVERLAP
    )

    text_sections = [
        split_page_contents_by_words[
            i : i + max_words_per_summary_section + WORDS_OVERLAP
        ]
        for i in range(
            0, len(split_page_contents_by_words), max_words_per_summary_section
        )
    ]

    truncated_text_sections = text_sections[:MAX_NUMBER_OF_TEXT_SECTIONS]

    summary = await _summarise_piecewise_with_questions(
        openai_api_key=openai_api_key,
        questions=questions,
        text_sections=truncated_text_sections,
    )

    logging.info(f"Summary of {url}: {summary}")

    return summary


async def _summarise_piecewise_with_questions(
    openai_api_key: str,
    questions: str,
    text_sections: list[str],
):
    if len(text_sections) == 0:
        return "NOT_RELEVANT"

    if len(text_sections) == 1:
        return await _summarise_with_questions(
            openai_api_key=openai_api_key,
            questions=questions,
            text=text_sections[0],
        )

    coroutines = []
    for text in text_sections:
        text = text.strip()

        if len(text) == 0:
            continue

        coroutines.append(
            _summarise_with_questions(
                openai_api_key=openai_api_key,
                questions=questions,
                text=text,
            )
        )

    summaries = await asyncio.gather(*coroutines)

    cleaned_summaries = [item for item in summaries if item != "NOT_RELEVANT"]
    combined_summaries = "\n\n".join(cleaned_summaries)

    summary = await _summarise_with_questions(
        openai_api_key=openai_api_key,
        questions=questions,
        text=combined_summaries,
    )

    return summary


async def _summarise_with_questions(openai_api_key: str, questions: str, text: str):
    prompt = PROMPT.format(questions=questions, text=text)

    completions = await completion_with_back_off(
        prompt=prompt, api_key=openai_api_key, **MODEL_KWARGS
    )
    response: str = completions.choices[0].text.strip()

    return response
