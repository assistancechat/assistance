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

import logging

from git.repo import Repo
from git.util import Actor
from git.exc import HookExecutionError

from assistance._paths import MONOREPO


def pull():
    repo = Repo(MONOREPO)
    _recursive_pull(repo)


def push(message: str):
    logging.info(f"Creating commits with message: {message}")

    repo = Repo(MONOREPO)
    _recursive_push(repo, message)


def _recursive_pull(repo: Repo):
    logging.info(f"Pulling: {repo.remotes.origin.url}")

    repo.remotes.origin.pull()

    for submodule in repo.submodules:
        _recursive_pull(submodule.module())


def _recursive_push(repo: Repo, message: str):
    for submodule in repo.submodules:
        _recursive_push(submodule.module(), message)

    if not repo.is_dirty(untracked_files=True):
        return

    repo.git.add(A=True)

    committer = Actor("Refuge Bot", "bot@refuge.au")

    try:
        repo.index.commit(message, author=committer, committer=committer)
    except HookExecutionError:
        repo.git.add(A=True)

        if not repo.is_dirty(untracked_files=True):
            return

        repo.index.commit(message, author=committer, committer=committer)

    logging.info(f"Pushing: {repo.remotes.origin.url}")
    repo.remotes.origin.push()
