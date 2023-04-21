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
    file_path = ""

    def __init__(self: "FakeResponse", url: str):  # noqa
        self.url = url

    async def read(self: "FakeResponse") -> bytes:
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
    async def test_worker_bad_response(self: "TestCrawler", url1: str):
        rules = [
            ["tbody", "a", {"href", "title"}],
        ]
        crawler = TCrawler(url1, rules)
        FakeResponse.status = 400
        await crawler.get_result()
        assert crawler.base_url.get_uri == crawler.errors_links.pop()

    async def test_worker_download_file(self: "TestCrawler", file_test: str):
        rules = [["tbody", "a", {"href", "title"}]]
        url = (
            "https://github.com/VIVERA83/crawler/archive/refs/heads/master.zip"
        )
        crawler = TCrawler(url, rules)
        FakeResponse.status = 200
        FakeResponse.content_type = "application/zip"
        FakeResponse.file_path = file_test
        assert len(await crawler.get_result()) == 1

    async def test_worker_download_text_file(
        self: "TestCrawler", file_page: str
    ):
        rules = [["tbody", "a", {"href", "title"}]]
        url = "https://github.com/VIVERA83/crawler/master.html"
        crawler = TCrawler(url, rules)
        FakeResponse.status = 200
        FakeResponse.content_type = "text/plain"
        FakeResponse.file_path = file_page
        assert len(await crawler.get_result()) == 1
