from typing import Optional

import aiofiles

from app.core.crawler import Crawler


class TTestClientSession:
    """Затычка ClientSession"""

    def __init__(self: "TTestClientSession") -> None:
        self.get = FakeResponse
        self.closed = True


class TCrawler(Crawler):
    session: Optional["TTestClientSession"] = None

    async def start(self: "Crawler") -> None:
        """
        Метод отвечает за подготовку для начала обкачки сайта
        :return:
        """
        await super().start()
        self.session = TTestClientSession()


class FakeResponse:
    status = 200
    content_type = "application/json"

    def __init__(self: "FakeResponse", url: str):  # noqa
        print(f"Creating Resp {url}")
        self.file_path = url

    async def read(self: "FakeResponse") -> bytes:
        print("Reading111111111111111")
        async with aiofiles.open(self.file_path, "rb") as file:
            return await file.read()

    async def __aenter__(self: "FakeResponse") -> "FakeResponse":
        return self

    async def __aexit__(
        self: "FakeResponse",
        exc_type: Exception,
        exc_value: str,
        traceback: str,
    ) -> None:
        return None


class TestCrawler:
    async def test_worker(self: "TestCrawler", url1: str):
        rules = [
            ["tbody", "a", {"href", "title"}],
        ]
        crawler = TCrawler(url1, rules)
        FakeResponse.status = 400
        await crawler.get_result()
        print(crawler.base_url.get_uri)
        assert crawler.base_url.get_uri == crawler.errors_links.pop()
