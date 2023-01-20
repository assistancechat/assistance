# Copyright (C) 2022 Assistance.Chat contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
import pathlib
import time

import aiofiles
import git

from .paths import RECORDS


async def store_prompt_transcript(
    record_grouping: str, username: str, model_kwargs: dict, prompt: str, response: str
):
    record_directory = _create_record_directory_with_epoch(
        RECORDS, [record_grouping, username, "transcripts"]
    )

    data_to_save = {
        "model-kwargs.json": json.dumps(model_kwargs, indent=2),
        "prompt.txt": prompt,
        "response.txt": response,
    }

    asyncio.create_task(
        _store_files_as_well_as_commit_hash(record_directory, data_to_save)
    )


def store_search_result(
    record_grouping: str, username: str, model_kwargs: dict, prompt: str, response: str
):
    pass


# TODO: This function should be able to assume that the filename isn't
# malicious, deal with sanitisation right next to the API interface
# instead of handling it within each function.
async def store_file(dirnames: list[str], filename: str, contents: str):
    directory = _create_record_directory_with_epoch(RECORDS, dirnames)

    # Just to validate that the provided filename is not malicious
    _build_path_tree_while_validating_no_traversal(directory, [filename])

    data_to_save = {filename: contents}

    asyncio.create_task(_store_files_as_well_as_commit_hash(directory, data_to_save))


async def _store_files_as_well_as_commit_hash(
    record_directory: pathlib.Path, data_to_save: dict[str, str]
):
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    data_to_save["git-hash.txt"] = sha

    for filename, contents in data_to_save.items():
        path = record_directory / filename

        async with aiofiles.open(path, "w") as f:
            await f.write(contents)


def _create_record_directory_with_epoch(root: pathlib.Path, dirnames: list[str]):
    epoch_time = str(time.time_ns())
    record_directory = (
        _build_path_tree_while_validating_no_traversal(root, dirnames) / epoch_time
    )

    record_directory.mkdir(exist_ok=True, parents=True)

    return record_directory


# TODO: Likely best to instead validate the path right at the API interface
def _build_path_tree_while_validating_no_traversal(
    root_path: pathlib.Path, filepath: list[str]
):
    new_path = root_path

    for item in filepath:
        prev_path = new_path
        new_path = prev_path / item

        resolved_prev_path = prev_path.resolve()
        resolved_new_path = new_path.resolve()

        if resolved_prev_path.parts != resolved_new_path.parts[:-1]:
            raise ValueError(f"Apparent path traversal attempt. {prev_path} / {item}")

    return new_path
