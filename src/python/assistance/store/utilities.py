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

import pathlib
import time

import aiofiles
import git


async def store_files_as_well_as_commit_hash(
    record_directory: pathlib.Path, data_to_save: dict[str, str]
):
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    data_to_save["git-hash.txt"] = sha

    for filename, contents in data_to_save.items():
        path = record_directory / filename

        async with aiofiles.open(path, "w") as f:
            await f.write(contents)


def create_record_directory_with_epoch(root: pathlib.Path, dirnames: list[str]):
    epoch_time = str(time.time_ns())
    record_directory = (
        build_path_tree_while_validating_no_traversal(root, dirnames) / epoch_time
    )

    record_directory.mkdir(exist_ok=True, parents=True)

    return record_directory


# TODO: Likely best to instead validate the path right at the API interface
def build_path_tree_while_validating_no_traversal(
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
