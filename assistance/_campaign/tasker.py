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
import tomllib
import json

from git.repo import Repo
from git.util import Actor
from git.exc import HookExecutionError

from assistance._paths import MONOREPO
from assistance._campaign import send

from . import stats


async def run_campaign():
    _pull()
    await _campaign()

    stats.run_stats()

    _push("Push of data after campaign run")


def _pull():
    repo = Repo(MONOREPO)
    _recursive_pull(repo)


def _push(message: str):
    repo = Repo(MONOREPO)
    _recursive_push(repo, message)


async def _campaign():
    base_cfg_path = MONOREPO / "shared" / "jims" / "config.toml"
    campaign_cfg_path = MONOREPO / "shared" / "jims" / "campaign.toml"

    with open(base_cfg_path, "rb") as f:
        base_cfg = tomllib.load(f)

    with open(campaign_cfg_path, "rb") as f:
        campaign_cfg = {
            **base_cfg,
            **tomllib.load(f),
        }

    (
        all_eoi_emails,
        emails_to_remove,
        started_application_emails,
        _incomplete_applications,
        name_lookup,
    ) = await send._get_email_segments_and_name_lookup()

    campaign_email_list = (
        set(all_eoi_emails)
        .difference(started_application_emails)
        .difference(emails_to_remove)
    )

    results = await send.campaign_workflow(
        campaign_cfg,
        name_lookup=name_lookup,
        email_list=campaign_email_list,
        dry_run=True,
    )

    logging.info(f"Results: {json.dumps(results, indent=2)}")


def _recursive_pull(repo: Repo):
    logging.info(f"Pulling: {repo.remotes.origin.url}")

    repo.remotes.origin.pull()

    for submodule in repo.submodules:
        _recursive_pull(submodule.module())


def _recursive_push(repo: Repo, message: str):
    for submodule in repo.submodules:
        _recursive_push(submodule.module(), message)

    logging.info(f"Adding and committing changes in: {repo.remotes.origin.url}")

    repo.git.add(A=True)

    committer = Actor("Refuge Bot", "bot@refuge.au")

    try:
        repo.index.commit(message, author=committer, committer=committer)
    except HookExecutionError:
        repo.git.add(A=True)
        repo.index.commit(message, author=committer, committer=committer)

    logging.info(f"Pushing: {repo.remotes.origin.url}")
    repo.remotes.origin.push()
