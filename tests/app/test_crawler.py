import asyncio

from aiohttp import ClientSession
from asyncio import TimeoutError

from app.core.crawler import Crawler
import pytest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


class TestCrawler:
    # @patch("aiohttp.ClientSession.get")
    # @pytest.mark.asyncio
    async def test_start(self, page_2):
        url = "https://github.com/VIVERA83/crawler"
        rules = [["turbo-frame", "a", {"href", "itemprop"}]]  # noqa
        crawler = Crawler(url, rules)
        await crawler.start()
        assert await crawler.links.get() == "/VIVERA83/crawler"
        assert len(crawler.workers) == 5
        assert crawler.is_running == True
        await crawler.get_result()

        # mock = ClientSession
        # mock.get = MagicMock()
        # mock.get.return_value.__aenter__.return_value.status = 200
        # mock.get.return_value.__aenter__.return_value.text.return_value = page_2
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(crawler.get_result(), 0)
