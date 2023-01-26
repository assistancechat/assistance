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

# pylint: disable = import-outside-toplevel

import typer

app = typer.Typer()


@app.command()
def start():
    from multiprocessing import Process

    Process(target=api).start()
    Process(target=admin).start()


@app.command()
def api():
    from assistance._api.main import main as _main

    _main()


@app.command()
def schema(path: str):
    import json

    from assistance._api.main import app as _app

    openapi_schema = _app.openapi()

    with open(path, "w", encoding="utf8") as f:
        json.dump(openapi_schema, f, indent=2)


@app.command()
def admin():
    from streamlit import config
    from streamlit.web import bootstrap

    from assistance._paths import LIB

    config.set_option("server.address", "localhost")
    config.set_option("browser.gatherUsageStats", False)
    config.set_option("server.port", 8501)

    bootstrap.run(
        str(LIB / "_admin" / "app.py"),
        command_line=None,
        args=[],
        flag_options={},
    )
