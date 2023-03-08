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


async def run_with_summary_fallback(
    scope: str,
    prompt: str,
    email_thread: list[str],
    api_key: str,
    **kwargs,
):
    while True:
        transcript = "\n\n".join(email_thread)
        prompt_with_transcript = prompt.replace("{transcript}", transcript)

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

            transcript_to_summarise = "\n\n".join(email_thread[0:5])

            summary = await get_completion_only(
                scope=scope,
                prompt=PROMPT.format(transcript=transcript_to_summarise),
                api_key=api_key,
                **kwargs,
            )

            summary_item = f"Summary of omitted emails:\n{summary}\n\n"
            email_thread = [summary_item] + email_thread[5:]

            continue

        break

    return response
