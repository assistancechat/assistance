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

from langchain import OpenAI
from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory

from .tools import alphacrucis_faq_search, alphacrucis_main_page_search


def create_agent_chain():
    tools = [
        Tool(
            name="Alphacrusis FAQ Search",
            func=alphacrucis_faq_search().run,
            description=(
                "useful for when you want to answer questions that may "
                "have been previously been asked to Alphacrusis "
                "support staff"
            ),
        ),
        Tool(
            name="Alphacrusis Main Page Search",
            func=alphacrucis_main_page_search().run,
            description=(
                "useful for when you want to answer questions that may "
                "be able to be found by searching Alphacrusis' website."
            ),
        ),
    ]

    memory = ConversationSummaryBufferMemory(memory_key="chat_history")

    llm = OpenAI(temperature=0)
    agent_chain = initialize_agent(
        tools,
        llm,
        agent="conversational-react-description",
        verbose=True,
        memory=memory,
    )

    return agent_chain
