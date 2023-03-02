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
    "max_tokens": 1024,
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
        and it is your job to select the {number_of_tools} best tools along with their
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

        def iterate_executive_function_system(<number of tasks>)
            \"""This allows you to re-run this executive function system
            with a requested number of extra tasks.

            Use this in the following situations:
            - You would like to call more tools than have been asked of
              you in this current iteration of the executive function.
            - There may be other tools you'd like to call, but your not
              sure until you see the results of the current tools you
              have requested.
            \"""


        # The task for the AI cluster

        {task}


        # Response Requirements

        - Your response must be valid JSON. It must be a list of {number_of_tools}
          dictionaries, with the keys "id",
          "step_by_step_thought_process", "tool", "args", "score", and
          "confidence".
        - Before writing any lines of the JSON you validate that what
          you are about to write is valid JSON.
        - Do not include comments in the JSON response, as that is not
          valid JSON.
        - If you would like to use the result of one tool as the input
          for another tool, you must specify the "depends_on" key in
          the dictionary for the tool that depends on the other tool.
        - To use the output of one tool as the input for another tool,
          use the id of the requested output within "moustache" brackets
          {{<tool request id goes here>}}.

        # Example response format for 6 tools. You MUST provide {number_of_tools} tools.

        [
            {{
                "id": 0,
                "step_by_step_thought_process": "I will start by using the 'now' tool to get the current date and time.",
                "tool": "now",
                "args": [],
                "score": 9,
                "confidence": 8
                "depends_on": []
            }},
            {{
                "id": 1,
                "step_by_step_thought_process": "The user asked what @phirho's preferred name was, let's search the 'phirho_memory' database for that.",
                "tool": "ai_embeddings_search",
                "args": ["phirho_memory", "phirho's preferred name"],
                "score": 8,
                "confidence": 7
                "depends_on": []
            }},
            {{
                "id": 2,
                "step_by_step_thought_process": "I want to make sure what I am saying is said in a way that is similar to how Philip would say it if it was him, so I will use the 'philip_rhoades_memory' database to search for that.",
                "tool": "ai_embeddings_search",
                "args": ["philip_rhoades_memory", "Responding to a being asked what your preferred name is."],
                "score": 9,
                "confidence": 5
                "depends_on": []
            }},
            {{
                "id": 3,
                "step_by_step_thought_process": "The user also asked how old I was, to do that I need to determine on what date I was born from my memory, and then I need to pass that through to the Python function.",
                "tool": "ai_embeddings_search",
                "args": ["phirho_memory", "phirho's birth date"],
                "score": 9,
                "confidence": 5
                "depends_on": []
            }},
            {{
                "id": 4,
                "step_by_step_thought_process": "I will use this tool to determine how old I am. I will use the Python function to subtract the date I was born from the current date.",
                "tool": "python",
                "args": ["from datetime import datetime; datetime.strptime(\\"{{0}}\\", \\"%Y-%m-%d %H:%M:%S\\") - datetime.strptime(\\"{{3}}\\", \\"%Y-%m-%d %H:%M:%S\\"))"],
                "score": 9,
                "confidence": 9
                "depends_on": [3, 0]
            }},
            {{
                "id": 5,
                "step_by_step_thought_process": "Given I have run a few searches, I want to take the opportunity to potentially call a few more functions once I have seen their results.",
                "tool": "iterate_executive_function_system",
                "args": [3],
                "score": 4,
                "confidence": 4
                "depends_on": []
            }},
        ]
        {previous_tool_iterations}{optional_previous_results_text}
        # Your JSON Response (MUST be valid JSON, do not include comments)
    """
).strip()


class AiToolRequest(TypedDict):
    id: int
    step_by_step_thought_process: str
    tool: str
    args: list[str]
    score: int
    confidence: int
    depends_on: list[int]

    # TODO: Maybe change this
    result: str


FAILED_ATTEMPT_TEMPLATE = textwrap.dedent(
    """
        # Previous attempt

        You previously submitted the following JSON tools request:

        {previous_request}

        But it resulted in the following error message:

        {error_message}

        Please try again.
    """
).strip()


PREVIOUS_RESULTS_TEMPLATE = textwrap.dedent(
    """
        # Previous iterations of this executive function system has given the following results

        {tools_string}

        For your remaining tools please start your index at {next_index}.
    """
).strip()


async def get_tools_and_responses(
    scope: str,
    task: str,
    number_of_tools: int = 3,
    previous_results: None | list[AiToolRequest] = None,
):
    optional_previous_results_text = ""
    if previous_results is not None:
        tools_string = json.dumps(previous_results, indent=2)
        previous_tool_iterations = PREVIOUS_RESULTS_TEMPLATE.format(
            tools_string=tools_string, next_index=len(previous_results)
        )
    else:
        previous_tool_iterations = ""

    while True:
        prompt = PROMPT.format(
            task=task,
            optional_previous_results_text=optional_previous_results_text,
            number_of_tools=number_of_tools,
            previous_tool_iterations=previous_tool_iterations,
        )

        response = await get_completion_only(
            scope=scope,
            prompt=prompt,
            api_key=OPEN_AI_API_KEY,
            **MODEL_KWARGS,
        )

        try:
            tools, number_of_new_tools_to_run = await _evaluate_tools(scope, response)
        except Exception as e:
            optional_previous_results_text = (
                "\n"
                + FAILED_ATTEMPT_TEMPLATE.format(
                    previous_request=response, error_message=str(e)
                )
                + "\n"
            )

            continue

        break

    if number_of_new_tools_to_run > 0:
        tools = await get_tools_and_responses(
            scope=scope,
            task=task,
            number_of_tools=number_of_new_tools_to_run,
            previous_results=tools,
        )

    return tools


async def _evaluate_tools(scope, response):
    try:
        tools: list[AiToolRequest] = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(f"Response is not valid JSON: {response}")

    number_of_new_tools_to_run = 0

    for tool in tools:
        tool_name = tool["tool"]
        tool_args = tool["args"]

        tool_dependencies = tool["depends_on"]
        if len(tool_dependencies) > 0:
            input_formatting = {}
            for dependency in tool_dependencies:
                input_formatting[dependency] = tools[dependency]["result"]

            tool_args = [arg.format(input_formatting) for arg in tool_args]

        args = [scope] + tool_args

        try:
            if tool_name == "iterate_executive_function_system":
                number_of_new_tools_to_run = max(number_of_new_tools_to_run, args[0])

                continue

            tool["result"] = await TOOLS[tool_name](*args)
        except Exception as e:
            raise ValueError(
                scope, f"Error running tool `{tool_name}` with args {tool_args}: {e}"
            )

    return tools, number_of_new_tools_to_run


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
