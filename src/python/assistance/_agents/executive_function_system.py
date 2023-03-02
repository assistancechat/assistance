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
from zoneinfo import ZoneInfo

from assistance import _ctx
from assistance._completions import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._types import Email

OPEN_AI_API_KEY = get_openai_api_key()
SERP_API_KEY = get_serp_api_key()


MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 2,
    "presence_penalty": 2,
}

PROMPT = textwrap.dedent(
    """
        # Your Purpose

        You are an Executive Function System for an AI cluster. You are
        provided with a task that other AI systems are going to execute,
        and it is your job to select the 10 best tools along with their
        corresponding inputs that can help them be successful in their
        task.


        # Your Available Tools

        Here are the tools available to your cluster:

        def internet_search('<string query>')
            \"""This returns a web search result for the given string argument.\"""

        def python(\"""<any python expression>\""")
            \"""This allows you to evaluate expressions using python.\"""

        def now()
            \"""This returns the current date and time.

            This tool takes no input args. Provide only an empty list
            for the args for this tool.
            \"""

        def ai_embeddings_search('<database_name>', '<text to search for within the database>')
            \"""This allows you to search a range of AI embeddings
            databases for the given string argument.

            The current supported databases are:
            - 'philip_rhoades_memory'
            - 'phirho_memory'
            - 'discourse_history'

            \"""


        # The task for the AI cluster

        {task}


        # Required JSON Response Format:

        [
            {{
                "id": 0,
                "step-by-step-thought-process": "<your thoughts for why this tool is needed, with new lines written as \\n>",
                "tool": "<the name of the tool>",
                "args": ["<the first input to the tool, with new lines written as \\n>", "the second input (if the tool has a second input)"],
                "score": <the score of the usefulness of this tool / inputs combination given the other tools that have already been requested, between 0 and 1>,
                "confidence": <the confidence that you have in your score, between 0 and 1>
            }},
            {{
                "id": 1,
                ...
            }},

            ...

            {{
                "id": 9,
                ...
            }}
        ]

        # Your JSON Response
    """
).strip()


async def get_tools_and_responses(scope: str, task: str):
    prompt = PROMPT.format(task=task)

    response = await get_completion_only(
        scope=scope,
        prompt=prompt,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    tools = json.loads(response)

    for tool in tools:
        tool_name = tool["tool"]
        tool_args = tool["args"]

        tool["response"] = await TOOLS[tool_name](*tool_args)

    return tools


async def _run_search(scope: str, query):
    params = {
        "location": "New+South+Wales,+Australia",
        "hl": "en",
        "gl": "au",
        "google_domain": "google.com.au",
        "q": query,
        "api_key": SERP_API_KEY,
    }

    url = "https://serpapi.com/search"

    response = await _ctx.session.get(url=url, params=params)

    results = await response.json()

    log_info(scope, json.dumps(results, indent=2))

    organic_results = results["organic_results"]

    snippets = []
    for item in organic_results:
        if "snippet" in item:
            snippets.append(item["snippet"])

    return " ".join(snippets)


async def _not_implemented(*args, **kwargs):
    return "Tool not yet implemented"


async def _get_current_date_and_time(*args, **kwargs):
    return datetime.now(tz=ZoneInfo("Australia/Sydney")).strftime("%Y-%m-%d %H:%M:%S")


TOOLS = {
    "internet_search": _run_search,
    "python": _not_implemented,
    "now": _get_current_date_and_time,
    "ai_embeddings_search": _not_implemented,
}
