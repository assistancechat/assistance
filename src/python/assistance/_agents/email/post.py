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

import textwrap

from assistance._agents.summaries import summarise_news_article_url_with_tasks
from assistance._completions import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL
from assistance._keys import get_openai_api_key
from assistance._utilities import items_to_list_string

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 2048,
    "best_of": 1,
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

        Your target audience:

        {target_audience}

        Your instructions:

        - Write as if you are speaking directly to the target audience,
          in second person.
        - DO NOT state or restate who the target audience is within your
          post. Assume that it is already known and they are the ones
          currently reading your post. Address them directly in second
          person.
        - DO NOT address the reader by their target audience definition.
        - You are not aiming to sell anything, instead just be
          informative. If the article is a "puff piece" make sure not to
          buy into the hype. Instead, be truthful and provide a balanced
          view while still being enthusiastic in your writing and making
          your post interesting and engaging.
        - If there isn't ample information within the article to work
          from, set "article-is-relevant" to false.
        - Make sure your post contains all the relevant information
          regarding the tasks. The reader should not need to read the
          article. Nor are you wanting them to actually read the
          article.
        - Fulfil each task in its own paragraph.

        The article of text you have been provided is:

        {text}

        Required JSON response format:

        {{
            "article-is-relevant": [true or false],
            "subject": "<Post subject goes here>",
            "content": "<Post content goes here, include new lines as \\n>"
        }}

        JSON response:
    """
).strip()


async def write_news_post(
    scope: str,
    openai_api_key: str,
    tasks: list[str],
    goals: list[str],
    target_audience: str,
    url: str,
) -> str:
    summary = await summarise_news_article_url_with_tasks(
        scope=scope,
        openai_api_key=openai_api_key,
        tasks=tasks,
        goals=goals,
        target_audience=target_audience,
        url=url,
    )

    prompt = PROMPT.format(
        tasks=items_to_list_string(tasks),
        goals=items_to_list_string(goals),
        target_audience=target_audience,
        text=summary,
    )

    response = await get_completion_only(
        scope=scope, prompt=prompt, api_key=openai_api_key, **MODEL_KWARGS
    )

    return response
