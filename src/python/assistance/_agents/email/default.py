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
from assistance._config import ROOT_DOMAIN

DEFAULT_TASKS = {
    "create": (
        "Used to create new agents. "
        "When emailing need to provide an agent name and a prompt.",
        None,
    )
}

_task_overviews = ""
for agent, (overview, _prompt) in DEFAULT_TASKS.items():
    _task_overviews += f"- {agent}@{ROOT_DOMAIN}: {overview}\n"


HI_TASK = (
    (
        "Used to onboard new users",
        textwrap.dedent(
            """
            You are the user's first port of call to using {ROOT_DOMAIN}.
            You are to have a welcoming discussion with them and provide
            them with an overview of what can be done.

            Overview of the AI agent emails and what they can do:
            {task_overviews}
        """
        )
        .format(task_overviews=_task_overviews, ROOT_DOMAIN=ROOT_DOMAIN)
        .strip(),
    ),
)

DEFAULT_TASKS["hi"] = HI_TASK
