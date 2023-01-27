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


import functools
import re
import textwrap
import time
from typing import Callable, Coroutine

import streamlit as st

from . import apps as _apps
from . import categories as _categories
from . import getkeys


def get_url_app():
    try:
        return st.experimental_get_query_params()["app"][0]
    except KeyError:
        return "index"


def swap_app(app):
    st.experimental_set_query_params(app=app)

    st.session_state.app = app

    # Not sure why this is needed. The `set_query_params` doesn't
    # appear to work if a rerun is undergone immediately afterwards.
    time.sleep(0.01)
    st.experimental_rerun()


def index(application_options):
    _, central_header_column, _ = st.columns((1, 2, 1))

    title_filter = central_header_column.text_input("Filter")
    pattern = re.compile(f".*{title_filter}.*", re.IGNORECASE)

    num_columns = len(_categories.APPLICATION_CATEGORIES_BY_COLUMN.keys())
    columns = st.columns(num_columns)

    for (
        column_index,
        categories,
    ) in _categories.APPLICATION_CATEGORIES_BY_COLUMN.items():
        column = columns[column_index]

        for category in categories:
            applications_in_this_category = [
                item
                for item in application_options.items()
                if item[1].CATEGORY == category and pattern.match(item[1].TITLE)
            ]

            if not title_filter or applications_in_this_category:
                column.write(
                    f"""
                        ## {category}
                    """
                )

            if not applications_in_this_category and not title_filter:
                column.write("> *No applications are currently in this category.*")
                continue

            applications_in_this_category = sorted(
                applications_in_this_category, key=_application_sorting_key
            )

            for app_key, application in applications_in_this_category:
                if column.button(application.TITLE):
                    swap_app(app_key)


def _application_sorting_key(application):
    return application[1].TITLE.lower()


def _get_apps_from_module(module):
    apps = {
        item.replace("_", "-"): getattr(module, item)
        for item in dir(module)
        if not item.startswith("_")
    }

    return apps


async def main():
    getkeys.check_and_set_open_ai_key()

    st.session_state.app = get_url_app()

    apps = _get_apps_from_module(_apps)
    application_options = {**apps}

    if (
        st.session_state.app != "index"
        and not st.session_state.app in application_options.keys()
    ):
        swap_app("index")

    if st.session_state.app != "index":
        st.title(application_options[st.session_state.app].TITLE)

        docstring = application_options[st.session_state.app].main.__doc__
        if docstring is not None:
            docstring = textwrap.dedent(f"    {docstring}")
            st.write(docstring)

        if st.sidebar.button("Return to Index"):
            swap_app("index")

        st.sidebar.write("---")

    if st.session_state.app == "index":
        application_function = functools.partial(
            index, application_options=application_options
        )
    else:
        application_function = application_options[st.session_state.app].main

    await application_function()
