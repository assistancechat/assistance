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

import asyncio
import logging

from assistance import _ctx


def main():
    _ctx.open_session()

    from assistance._faq import tasker as _faq_tasker
    from assistance._campaign import tasker as _campaign_tasker

    loop = asyncio.get_event_loop()

    logging.info("Starting tasker")

    loop.run_forever()
