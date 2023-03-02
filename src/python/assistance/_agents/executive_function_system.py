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
    "max_tokens": 2048,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
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

        def python("<any python expression>")
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


        # Response Requirements

        - Your response must be valid JSON. It must be a list of 10
          dictionaries, with the keys "id",
          "step-by-step-thought-process", "tool", "args", "score", and
          "confidence".
        - Before writing any lines of the JSON you validate that what
          you are about to write is valid JSON.
        - Do not include comments in the JSON response, as that is not
          valid JSON.
        - If you would like to use the result of one tool as the input
          for another tool, you must specify the "depends-on" key in
          the dictionary for the tool that depends on the other tool.
        - To use the output of one tool as the input for another tool,
          use the id of the requested output within "mustach" brackets
          {{<tool request id goes here>}}.

        # Example response format for 5 tools. You MUST provide 10 tools.

        [
            {{
                "id": 0,
                "step-by-step-thought-process": "I will start by using the 'now' tool to get the current date and time.",
                "tool": "now",
                "args": [],
                "score": 9,
                "confidence": 8
                "depends-on": []
            }},
            {{
                "id": 1,
                "step-by-step-thought-process": "The user asked what @phirho's preferred name was, let's search the 'phirho_memory' database for that.",
                "tool": "ai_embeddings_search",
                "args": ["phirho_memory", "phirho's preferred name"],
                "score": 8,
                "confidence": 7
                "depends-on": []
            }},
            {{
                "id": 2,
                "step-by-step-thought-process": "I want to make sure what I am saying is said in a way that is similar to how Philip would say it if it was him, so I will use the 'philip_rhoades_memory' database to search for that.",
                "tool": "ai_embeddings_search",
                "args": ["philip_rhoades_memory", "Responding to a being asked what your preferred name is."],
                "score": 9,
                "confidence": 5
                "depends-on": []
            }},
            {{
                "id": 3,
                "step-by-step-thought-process": "The user also asked how old I was, to do that I need to determine on what date I was born from my memory, and then I need to pass that through to the Python function.",
                "tool": "ai_embeddings_search",
                "args": ["phirho_memory", "phirho's birth date"],
                "score": 9,
                "confidence": 5
                "depends-on": []
            }},
            {{
                "id": 4,
                "step-by-step-thought-process": "I will use this tool to determine how old I am. I will use the Python function to subtract the date I was born from the current date.",
                "tool": "python",
                "args": ["from datetime import datetime; datetime.strptime(\\"{{0}}\\", \\"%Y-%m-%d %H:%M:%S\\") - datetime.strptime(\\"{{3}}\\", \\"%Y-%m-%d %H:%M:%S\\"))"],
                "score": 9,
                "confidence": 9
                "depends-on": [3, 0]
            }}
        ]

        # Your JSON Response (MUST be valid JSON, do not include comments)
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

    try:
        tools = json.loads(response)
    except json.JSONDecodeError:
        log_info(scope, f"Response is not valid JSON: {response}")
        raise

    for tool in tools:
        tool_name = tool["tool"]
        tool_args = tool["args"]

        tool["result"] = await TOOLS[tool_name](*tool_args)

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
