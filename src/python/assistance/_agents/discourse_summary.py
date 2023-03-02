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

# Prompt inspired by the work provided under an MIT license over at:
# https://github.com/hwchase17/langchain/blob/ae1b589f60a/langchain/agents/conversational/prompt.py#L1-L36

import json
import re
import textwrap
from datetime import datetime
from typing import Any, TypedDict
from zoneinfo import ZoneInfo

import openai

from assistance import _ctx
from assistance._completions import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._types import Email

PROMPT = textwrap.dedent(
    """
        Write a summary of the following Discourse posts:

        {transcript}

        Go!
    """
).strip()


MAX_MODEL_TOKENS = 4096


class DiscoursePost(TypedDict):
    user: str
    content: str


async def run_with_summary_fallback(
    scope: str,
    prompt: str,
    discourse_posts: list[DiscoursePost],
    api_key: str,
    **kwargs,
):
    while True:
        transcript = _create_transcript_string(scope, discourse_posts[0:-1])
        most_recent = _create_transcript_string(scope, discourse_posts[-1:])
        prompt_with_transcript = prompt.replace("{transcript}", transcript).replace(
            "{most_recent_post}", most_recent
        )

        try:
            response = await get_completion_only(
                scope=scope,
                prompt=prompt_with_transcript,
                api_key=api_key,
                **kwargs,
            )
        except ValueError as e:
            if "Model maximum reached" not in str(e):
                raise e

            to_summarise = discourse_posts[0:5]
            transcript_to_summarise = _create_transcript_string(scope, to_summarise)

            summary = await get_completion_only(
                scope=scope,
                prompt=PROMPT.format(transcript=transcript_to_summarise),
                api_key=api_key,
                **kwargs,
            )

            summary_post: DiscoursePost = {
                "user": "Summary",
                "content": summary,
            }

            discourse_posts = [summary_post] + discourse_posts[5:]

            continue

        break

    return response


def _create_transcript_string(scope, discourse_posts: list[DiscoursePost]):
    transcript = ""
    for post in discourse_posts:
        try:
            user = post["user"]
        except KeyError as e:
            log_info(scope, f"Missing user in post: {post}")
            raise e

        if user == "Summary":
            transcript += f"Summary of some omitted posts:\n\n{post['content']}\n\n"
            continue

        transcript += f"Post from @{user}:\n{post['content']}\n\n"

    return transcript
