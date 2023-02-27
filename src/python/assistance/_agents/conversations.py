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

import asyncio
import re
import textwrap
from enum import Enum
from typing import Callable, Coroutine

from thefuzz import process as fuzz_process

from assistance._completions import get_completion_only
from assistance._logging import log_info
from assistance._store.transcript import store_prompt_transcript

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 512,
    "best_of": 1,
    "stop": "Observation:",
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.1,
    "presence_penalty": 0.1,
}


class Tool(str, Enum):
    SEARCH = "Alphacrucis Search and Summarise"
    EMAIL = "Email Supervisors"
    RESPOND = "Respond"


TOOL_DESCRIPTIONS = {
    # Tool.SEARCH: textwrap.dedent(
    #     """
    #         A tool where Assistant provides a natural language question.
    #         The tool initially searches the Alphacrucis student support
    #         FAQ page and the main website. After it has undergone a
    #         search a separate LLM will summarise the pages found with
    #         respect to relevance to the provided question.
    #     """
    # ).strip(),
    # Tool.EMAIL: textwrap.dedent(
    #     """
    #         A tool to send an email to the Assistant's Supervisors.
    #         Assistant may use this tool to seek help from the
    #         Assistant's supervisors if it is unsure how best to respond.
    #     """
    # ).strip(),
}


PROMPT = textwrap.dedent(
    """
        Assistant is a large language model (LLM).

        Assistant is designed to be able to assist with a wide range of
        tasks, from answering simple questions to providing in-depth
        explanations and discussions on a wide range of topics. As a
        language model, Assistant is able to generate human-like text
        based on the input it receives, allowing it to engage in
        natural-sounding conversations and provide responses that are
        coherent and relevant to the topic at hand.

        Assistant is constantly learning and improving, and its
        capabilities are constantly evolving. It is able to process and
        understand large amounts of text, and can use this knowledge to
        provide accurate and informative responses to a wide range of
        questions. Additionally, Assistant is able to generate its own
        text based on the input it receives, allowing it to engage in
        discussions and provide explanations and descriptions on a wide
        range of topics.

        Assistant is predicting {agent_name}'s responses within a
        conversation between {client_name} and {agent_name}. Assistant
        uses the tools, task description and the transcript of the
        conversation thus far that is detailed below to determine the
        most appropriate next response for {agent_name}.

        Assistant is never deceptive. Assistant always directs truthful
        responses. Assistant has Supervisors. If Assistant is unsure
        how best to appropriately respond and Assistant has exhausted
        all of the other relevant tools at its disposal, Assistant may
        reach out to its Supervisors using one of the Supervisor tools.

        Assistant aims to meet the desires of its Supervisors.

        Aims for {agent_name}:
        ----------------------

        {task_prompt}

        TOOLS:
        ------
        Assistant has access to the following tools:

        {tools_string}

        To use a tool, Assistant uses the following format:

        ```
        Thought: Does Assistant need to use a tool? Yes
        Action: The action to take, should be one of [{tool_names}]
        Action Input: The input to the action
        Observation: The result of the action
        ```

        When Assistant is ready to provide the response of {agent_name}
        or if Assistant does not need to use a tool, Assistant MUST use
        the format:

        ```
        Thought: Does Assistant need to use a tool? No
        {agent_name}: [Assistant's determined response for {agent_name} here]
        ```

        TRANSCRIPT THUS FAR:
        --------------------
        {transcript}

        Assistant Process:
        Thought: Does Assistant need to use a tool?
    """
).strip()


async def run_conversation(
    record_grouping: str,
    user_email: str,
    openai_api_key: str,
    task_prompt: str,
    agent_name: str,
    client_email: str,
    client_name: str,
    transcript: None | str = None,
):
    if not transcript:
        transcript = "Conversation has not yet begun"

    tools = []

    for tool, description in TOOL_DESCRIPTIONS.items():
        tools.append(f"{tool.value}: {description}")

    if len(tools) == 0:
        tools_string = "No tools available"
    else:
        tools_string = "\n".join(tools)

    tool_names = ", ".join(TOOL_DESCRIPTIONS.keys())

    task_prompt_with_replacements = task_prompt.format(
        agent_name=agent_name, client_name=client_name
    )
    transcript_with_replacements = transcript.format(
        agent_name=agent_name, client_name=client_name
    )

    prompt = PROMPT.format(
        task_prompt=task_prompt_with_replacements,
        agent_name=agent_name,
        client_name=client_name,
        tools_string=tools_string,
        tool_names=tool_names,
        transcript=transcript_with_replacements,
    )

    log_info(user_email, prompt)

    # async def _search(query: str):
    #     return await alphacrucis_search(
    #         openai_api_key=openai_api_key,
    #         record_grouping=record_grouping,
    #         client_email=client_email,
    #         query=query,
    #     )

    # async def _email(query: str):
    #     return "Unfortunately emailing the Supervisors is not currently available"

    tool_functions = {
        # Tool.SEARCH: _search,
        # Tool.EMAIL: _email,
    }

    response = await _run_llm_process_observation_loop(
        record_grouping=record_grouping,
        user_email=user_email,
        openai_api_key=openai_api_key,
        agent_name=agent_name,
        client_email=client_email,
        prompt=prompt,
        tool_functions=tool_functions,
    )

    return response


async def _run_llm_process_observation_loop(
    record_grouping: str,
    user_email: str,
    openai_api_key: str,
    agent_name: str,
    client_email: str,
    prompt: str,
    tool_functions: dict[Tool, Callable[[str], Coroutine]],
):
    response = ""
    no_tool_text = f"{agent_name}:"
    regex = r"Action: (.*?)\nAction Input: (.*)"

    available_tools = [item.value for item in tool_functions.keys()]

    while True:
        response = await _call_gpt_and_store_as_transcript(
            user_email=user_email,
            openai_api_key=openai_api_key,
            record_grouping=record_grouping,
            client_email=client_email,
            model_kwargs=MODEL_KWARGS,
            prompt=prompt,
        )

        if no_tool_text in response:
            break

        match = re.search(regex, response)
        if match is None:
            raise ValueError("Could not find action in response")

        action_requested = match.group(1)
        action_input = match.group(2)
        action_input = action_input.strip(" ").strip('"')

        matched_action = fuzz_process.extractOne(action_requested, available_tools)[0]
        action_function = tool_functions[Tool(matched_action)]

        observation_result = await action_function(action_input)
        prompt += f"Observation: {observation_result}\n"

    result = response.split(no_tool_text)[-1].strip()

    return result


async def _call_gpt_and_store_as_transcript(
    user_email: str,
    openai_api_key: str,
    record_grouping: str,
    client_email: str,
    model_kwargs: dict,
    prompt: str,
):
    response = await get_completion_only(
        scope=user_email,
        prompt=prompt,
        api_key=openai_api_key,
        **model_kwargs,
    )

    asyncio.create_task(
        store_prompt_transcript(
            record_grouping=record_grouping,
            client_email=client_email,
            model_kwargs=model_kwargs,
            prompt=prompt,
            response=response,
        )
    )

    return response
