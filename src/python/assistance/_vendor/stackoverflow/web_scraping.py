# This work is licensed under the Creative Commons
# Attribution-ShareAlike 4.0 International License.
# <http://creativecommons.org/licenses/by-sa/4.0/>.

import logging

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from assistance._logging import log_info
from assistance._paths import (
    get_article_metadata_path,
    get_downloaded_article_path,
    get_hash_digest,
)


# https://stackoverflow.com/a/24618186
async def scrape(session: aiohttp.ClientSession, url: str):
    html = await _scrape_with_cache(session, url)

    try:
        html.decode(encoding="utf8")
    except UnicodeDecodeError:
        return "NOT_RELEVANT"

    soup = BeautifulSoup(html, features="html.parser")

    # log_info(soup)

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


async def _scrape_with_cache(session: aiohttp.ClientSession, url: str):
    url_hash_digest = get_hash_digest(url)
    downloaded_article_path = get_downloaded_article_path(
        url_hash_digest, create_parent=True
    )

    # TODO: Remove this
    meta_data_path = get_article_metadata_path(url_hash_digest)

    if meta_data_path.exists():
        meta_data_path.rename(downloaded_article_path)
    # Down to here

    if downloaded_article_path.exists():
        logging.info(f"Using cached version of {url}")

        async with aiofiles.open(downloaded_article_path, "rb") as f:
            cached_results = await f.read()

        if b"Error 404" not in cached_results:
            return cached_results

    logging.info(f"Downloading {url}")

    results = await session.get(url=url)
    url_results = await results.read()

    if b"Our systems have detected unusual traffic" in url_results:
        raise ValueError(url_results)

    async with aiofiles.open(downloaded_article_path, "wb") as f:
        await f.write(url_results)

    if b"Error 404" not in url_results:
        return url_results

    return b"NOT_RELEVANT"
