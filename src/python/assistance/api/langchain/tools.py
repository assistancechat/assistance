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

from langchain.serpapi import SerpAPIWrapper

from ..keys import get_serp_api_key

API_KEY = get_serp_api_key()

# TODO: Swap these out for async calls
def alphacrucis_faq_search():
    search = _create_custom_site_search("https://intercom.help/ac-support/en/")

    return search


def alphacrucis_main_page_search():
    search = _create_custom_site_search("https://www.ac.edu.au/")

    return search


def _create_custom_site_search(url):
    search = SerpAPIWrapper(params={"gl": "au"}, serpapi_api_key=API_KEY)

    old_run = search.run

    def new_run(self, query: str) -> str:
        query = f"site:{url} {query}"
        return old_run(self, query=query)

    search.run = new_run

    return search
