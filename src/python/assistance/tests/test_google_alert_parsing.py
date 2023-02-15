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


import pathlib

HERE = pathlib.Path(__file__).parent
DATA = HERE / "data"

ALERTS_PATH = DATA / "google-alert-example.html"

from assistance._parsing import googlealerts


def test_google_alerts_parsing():
    with ALERTS_PATH.open("r") as f:
        html = f.read()

    article_details = googlealerts.parse_alerts(html)
    assert len(article_details) == 10

    assert article_details[0] == {
        "title": "Indian international students face accommodation 'nightmare' in Australia | SBS Punjabi",
        "description": "International students from India scramble to find places to live in Australia. \u00b7 Rising rental prices and lack of properties behind Australia's\u00a0...",
        "url": "https://www.google.com/url?rct=j&sa=t&url=https://www.sbs.com.au/language/punjabi/en/article/indian-international-students-face-accommodation-struggles-in-australia/xrymy2c91&ct=ga&cd={redacted}&usg=AOvVaw1lOeu-mv0kcVYEtd8sAz4m",
    }
