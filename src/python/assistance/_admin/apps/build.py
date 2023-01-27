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

import os
import pathlib

import openai
import streamlit as st

from assistance._admin import categories
from assistance._paths import LIB

CATEGORY = categories.DEMO
TITLE = "Create Streamlit apps with GPT"

GPT_PROMPT = """
You are an expert Streamlit programmer. You validate all of your code
after you write it. Take the description of a streamlit app below and
output the code to create a new Streamlit app. Contain all of the
application within a function called main.

The streamlit application is fully functional. The title on the page has
already been drawn in a separate function. Do not call the main()
function within the script, it will be called separately.

Do not write any code to set the openai API key. It has already been
done.

If ever using the openai library make sure to make use of the engine
called "text-davinci-003".

Only use Python libraries that would be made available by installing the
following requirements.txt file:
```
streamlit
numpy
scipy
requests
thefuzz
openai
```

App Title:
{app_title}

Description:
{app_description}

Fully functional streamlit app: ```python
"""

INJECTED_CODE = """
from assistance._admin import categories

CATEGORY = categories.AI_CREATIONS
TITLE = "{app_title}"
"""

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 2048,
    "best_of": 2,
    "stop": "```",
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}


def main():
    app_filename = st.text_input("Python filename for your app (eg. new.py)")
    if not app_filename:
        st.stop()

    apps_dir = LIB / "_admin" / "apps"
    app_path = apps_dir / app_filename
    init_path = apps_dir / "__init__.py"

    basename, file_extension = app_filename.split(".")

    if file_extension != "py":
        st.error(f"File extension must be .py")
        st.stop()

    if app_path.exists():
        st.info(f"{app_filename} already exists.")
        _write_link_to_app(basename)
        st.stop()

    app_title = st.text_input("App Title")
    app_description = st.text_area("App Description")

    if not st.button("Create App"):
        st.stop()

    prompt = GPT_PROMPT.format(app_title=app_title, app_description=app_description)
    completions = openai.Completion.create(prompt=prompt, **MODEL_KWARGS)
    response: str = completions.choices[0].text.strip()

    final_code = f"{INJECTED_CODE.format(app_title=app_title)}\n\n{response}"

    with open(app_path, "w") as f:
        f.write(final_code)

    with open(init_path) as f:
        previous_init = f.readline().strip()

    new_init = f"{previous_init}, {basename}\n"

    with open(init_path, "w") as f:
        f.write(new_init)

    _write_link_to_app(basename)


def _write_link_to_app(basename):
    st.markdown(f"Link to app: [{basename}](?app={basename})")
