# This work is licensed under the Creative Commons
# Attribution-ShareAlike 4.0 International License.
# <http://creativecommons.org/licenses/by-sa/4.0/>.

import logging

import aiofiles
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from assistance._paths import get_downloaded_article_path, get_hash_digest


# https://stackoverflow.com/a/24618186
async def scrape(session: aiohttp.ClientSession, url: str):
    html = await _scrape_with_cache(session, url)

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


async def _scrape_with_cache(session: aiohttp.ClientSession, url: str):
    url_hash_digest = get_hash_digest(url)
    downloaded_article_path = get_downloaded_article_path(
        url_hash_digest, create_parent=True
    )

    if downloaded_article_path.exists():
        logging.info(f"Using cached version of {url}")

        async with aiofiles.open(downloaded_article_path, "rb") as f:
            return await f.read()

    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    cached_url = (
        f"http://webcache.googleusercontent.com/search?q=cache:{url}&strip=1&vwsrc=0"
    )

    logging.info(f"Downloading {cached_url}")

    results = await session.get(url=cached_url, headers=headers)
    url_results = await results.read()

    decoded = url_results.decode(encoding="utf8")
    if "Our systems have detected unusual traffic" in decoded:
        raise ValueError(decoded)

    async with aiofiles.open(downloaded_article_path, "wb") as f:
        await f.write(url_results)

    return url_results
