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

import aiocron

from assistance._config import load_targeted_news_config
from assistance._news.process import process_articles

# TODO: Make a separate process that both runs the cron jobs.


@aiocron.crontab("50 8 * * *")
async def run_email_digest():
    cfg = await load_targeted_news_config()

    await process_articles(cfg)
