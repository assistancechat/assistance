# This work is licensed under the Creative Commons
# Attribution-ShareAlike 4.0 International License.
# <http://creativecommons.org/licenses/by-sa/4.0/>.

import logging

import aiohttp
from bs4 import BeautifulSoup


# https://stackoverflow.com/a/24618186
async def scrape(session: aiohttp.ClientSession, url: str):
    results = await session.get(url=url)
    html = await results.read()

    try:
        html.decode(encoding="utf8")
    except UnicodeDecodeError:
        return "NOT_RELEVANT"

    soup = BeautifulSoup(html, features="html.parser")

    # logging.info(soup)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text(separator="\n")

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text
