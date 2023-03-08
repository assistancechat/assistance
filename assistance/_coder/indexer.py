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

from assistance._utilities import get_hash_digest

EXAMPLE_DOCSTRING = textwrap.dedent(
    """
        Searches the internet for information related to the given query.

        Parameters
        ----------
        query : str
            The search query.

        Returns
        -------
        str
            A summary of the findings related to the query.
    """
).strip()


def hash_for_docstring(docstring: str) -> str:
    return get_hash_digest(docstring)
