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

from assistance._agents.summaries import summarise_news_article_url_with_tasks
from assistance._completions import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL
from assistance._keys import get_openai_api_key
from assistance._utilities import items_to_list_string

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}

OPEN_AI_API_KEY = get_openai_api_key()

PROMPT = textwrap.dedent(
    """
        You are aiming to write an engaging and truthful social media
        post about an article of text that you have been provided while
        fulfilling a series of detailed tasks.

        Within your post you are aiming to fulfil the following tasks and
        goals for the following target audience:

        Your tasks:

        {tasks}

        Your goals:

        {goals}

        Your target audience definition:

        {target_audience}

        Your instructions:

        - DO NOT provide headers titles for any of the task paragraphs.
        - DO NOT mention the target audience definition within your post.
        - Write as if you are speaking directly to the target audience,
          in second person.
        - You are not aiming to sell anything, instead just be
          informative. If the article is a "puff piece" make sure not to
          buy into the hype. Instead, be truthful and provide a balanced
          view while still being enthusiastic in your writing and making
          your post interesting and engaging.
        - If there isn't ample information within the article to work
          from, set "article_is_relevant" to false.
        - Make sure your post contains all the relevant information
          regarding the tasks. The reader should not need to read the
          article. Nor are you wanting them to actually read the
          article.
        - Fulfil each task in its own paragraph.
        {sentence_blacklist_prompt}
        The article of text you have been provided is:

        {text}

        Required JSON response format:

        {{
            "article_is_relevant": [true or false],
            "subject": "<Post subject goes here>",
            "things_to_consider": "<A list of things to consider goes here, include new lines as \\n>",
            "content": "<Post content goes here, include new lines as \\n>"
        }}

        JSON response:
    """
).strip()


SENTENCE_BLACKLIST = textwrap.dedent(
    """
        The following is a blacklist of sentences. Do not write these
        sentences, or anything similar, within your post.

        {sentence_blacklist}
    """
).strip()


async def write_news_post(
    scope: str,
    openai_api_key: str,
    tasks: list[str],
    goals: list[str],
    target_audience: str,
    sentence_blacklist: list[str],
    url: str,
    use_google_cache=True,
) -> tuple[str, str]:
    try:
        summary = await summarise_news_article_url_with_tasks(
            scope=scope,
            openai_api_key=openai_api_key,
            tasks=tasks,
            goals=goals,
            target_audience=target_audience,
            url=url,
            use_google_cache=use_google_cache,
        )
    except asyncio.TimeoutError:
        return "NOT_RELEVANT", '{"article_is_relevant": false}'

    if len(sentence_blacklist) > 0:
        sentence_blacklist_prompt = (
            "\n"
            + SENTENCE_BLACKLIST.format(
                sentence_blacklist=items_to_list_string(sentence_blacklist)
            )
            + "\n"
        )
    else:
        sentence_blacklist_prompt = ""

    prompt = PROMPT.format(
        tasks=items_to_list_string(tasks),
        goals=items_to_list_string(goals),
        target_audience=target_audience,
        sentence_blacklist_prompt=sentence_blacklist_prompt,
        text=summary,
    )

    response = await get_completion_only(
        scope=scope, prompt=prompt, api_key=openai_api_key, **MODEL_KWARGS
    )

    return summary, response
