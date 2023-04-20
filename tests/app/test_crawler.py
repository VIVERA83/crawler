import asyncio
from asyncio import TimeoutError

import pytest

from app.core.crawler import Crawler


class TestCrawler:
    async def test_start(self: "TestCrawler", page_2: str):
        url = "https://github.com/VIVERA83/crawler"
        rules = [["turbo-frame", "a", {"href", "itemprop"}]]  # noqa
        crawler = Crawler(url, rules)
        await crawler.start()
        assert await crawler.links.get() == "/VIVERA83/crawler"
        assert len(crawler.workers) == 5
        assert crawler.is_running
        await crawler.get_result()
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(crawler.get_result(), 0)
