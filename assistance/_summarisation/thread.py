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


import textwrap

from assistance._config import DEFAULT_OPENAI_MODEL
from assistance._openai import get_completion_only

SUMMARY_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


SUMMARY_PROMPT_WITH_INSTRUCTIONS = textwrap.dedent(
    """
        # Summarise with instructions

        Write a summary of the following email thread while following
        the given instructions.

        ## Instructions

        {instructions}

        ## Email transcript

        {transcript}

        ## Your Summary
    """
).strip()

SUMMARY_PROMPT_WITHOUT_INSTRUCTIONS = textwrap.dedent(
    """
        Write a summary of the following email thread:

        {transcript}

        Go!
    """
).strip()


MAX_MODEL_TOKENS = 4096

SUMMARY_BATCH_SIZE = 2


async def run_with_summary_fallback(
    scope: str,
    prompt: str,
    email_thread: list[str],
    api_key: str,
    instructions: str | None = None,
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

            transcript_to_summarise = "\n\n".join(email_thread[0:SUMMARY_BATCH_SIZE])

            if instructions:
                summary_prompt = SUMMARY_PROMPT_WITH_INSTRUCTIONS.format(
                    transcript=transcript_to_summarise, instructions=instructions
                )
            else:
                summary_prompt = SUMMARY_PROMPT_WITHOUT_INSTRUCTIONS.format(
                    transcript=transcript_to_summarise
                )

            summary = await get_completion_only(
                scope=scope,
                prompt=summary_prompt,
                api_key=api_key,
                **SUMMARY_KWARGS,
            )

            summary_item = f"Summary of omitted emails:\n{summary}\n\n"
            email_thread = [summary_item] + email_thread[SUMMARY_BATCH_SIZE:]

            continue

        break

    return response, transcript
