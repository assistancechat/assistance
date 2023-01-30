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
import textwrap
from enum import Enum

import openai

from assistance._agents.queries import query_from_transcript
from assistance._store.transcript import store_prompt_transcript
from assistance._tools.search import alphacrucis_search

RECORD_GROUPING = "student.assistance.chat"

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 1,
    "stop": ["Observation:", "PROCESS COMPLETE"],
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

# TODO: Pull this into the API and allow the task to be defined within
# the frontend.
TASK_DESCRIPTION = textwrap.dedent(
    """
        {agent_name} is a student assistant who is helping students
        find out more about the Alphacrucis Christian University while
        also potentially helping them to undergo enrolment.

        The Supervisors want this conversation to be where
        {client_name} gets their information. As such, please don't
        redirect them to external sources.

        If appropriate the Supervisors want {client_name} to sign
        up to an Alphacrucis University course through having this
        conversation with {agent_name}.

        If relevant, it is {agent_name}'s goal to sell a course to
        {client_name}.

        {agent_name} is to always be polite and helpful. Even when
        talked to inappropriately.
    """
).strip()


class Tool(str, Enum):
    SEARCH = "Alphacrucis Search and Summarise"
    EMAIL = "Email Supervisors"
    RESPOND = "Respond"


TOOLS = {
    Tool.SEARCH: textwrap.dedent(
        """
            A tool where Assistant provides a natural language question.
            The tool initially searches the Alphacrucis student support
            FAQ page and the main website. After it has undergone a
            search a separate LLM will summarise the pages found with
            respect to relevance to the provided question.
        """
    ).strip(),
    Tool.EMAIL: textwrap.dedent(
        """
            A tool to send an email to the Assistant's Supervisors.
            Assistant may use this tool to seek help from the
            Assistant's supervisors if it is unsure how best to respond.
        """
    ).strip(),
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

        TASK FOR THE CONVERSATION:
        --------------------------
        Here are the Supervisors' task for the Assistant

        {task_description}

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

        PROCESS COMPLETE
        ```

        TRANSCRIPT THUS FAR:
        --------------------
        {transcript}

        Assistant Process:
        Thought: Does Assistant need to use a tool?
    """
).strip()


async def run_student_chat(
    agent_name: str, username: str, client_name: str, transcript: None | str = None
):
    if not transcript:
        transcript = "Conversation has not yet begun"

    else:
        query = await query_from_transcript(
            record_grouping=RECORD_GROUPING, username=username, transcript=transcript
        )

        additional_information = await alphacrucis_search(
            record_grouping=RECORD_GROUPING, username=username, query=query
        )

    tools = []

    for tool, description in TOOLS.items():
        tools.append(f"{tool}: {description}")

    tools_string = "\n".join(tools)
    tool_names = ", ".join(TOOLS.keys())

    prompt_template = PROMPT.format(task_description=TASK_DESCRIPTION)

    prompt = prompt_template.format(
        agent_name=agent_name,
        client_name=client_name,
        tools_string=tools_string,
        tool_names=tool_names,
        transcript=transcript,
    )

    response = await _run_tool_chaining(username=username, prompt=prompt)

    return response


async def _run_llm_process_observation_loop(
    agent_name: str, username: str, prompt: str
):
    response = ""

    no_tool_text = f"No\n{agent_name}: "

    while no_tool_text in response:
        response = await _call_gpt_and_store_as_transcript(
            record_grouping=RECORD_GROUPING,
            username=username,
            model_kwargs=MODEL_KWARGS,
            prompt=prompt,
        )

    result = response.split(no_tool_text)[-1]

    return result


async def _call_gpt_and_store_as_transcript(
    record_grouping: str,
    username: str,
    model_kwargs: dict,
    prompt: str,
):
    completions = await openai.Completion.acreate(prompt=prompt, **model_kwargs)
    response: str = completions.choices[0].text.strip()

    asyncio.create_task(
        store_prompt_transcript(
            record_grouping=record_grouping,
            username=username,
            model_kwargs=model_kwargs,
            prompt=prompt,
            response=response,
        )
    )

    return response
