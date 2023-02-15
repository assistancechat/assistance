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

import bs4


def parse_alerts(html):
    soup = bs4.BeautifulSoup(html, "html.parser")

    soup_articles = [
        item for item in soup.find_all("tr", itemtype="http://schema.org/Article")
    ]

    article_details = []
    for soup_article in soup_articles:
        article_details.append(
            {
                "title": _clean(soup_article.find("span", itemprop="name")),
                "description": _clean(soup_article.find("div", itemprop="description")),
                "url": soup_article.find("a", itemprop="url")["href"],
            }
        )

    # print(json.dumps(article_details, indent=2))

    return article_details


def _clean(soup):
    text = soup.get_text(separator="\n")

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = " ".join(chunk for chunk in chunks if chunk)

    return text
