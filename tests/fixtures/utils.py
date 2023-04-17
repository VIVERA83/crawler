import asyncio

import aiofiles
import pytest
from aiohttp import ClientResponse


class Resp(ClientResponse):
    def __init__(self, file_path):  # noqa
        self.file_path = file_path

    async def read(self) -> bytes:
        async with aiofiles.open(self.file_path, "rb") as f:
            return await f.read()


class RespCancel(Resp):
    async def read(self):
        await asyncio.sleep(3)


class RespText(Resp):
    text = b"Hello world!"

    async def read(self) -> bytes:
        return self.text

    @property
    def len(self):
        return len(self.text)


@pytest.fixture
def resp(base_path, file_page) -> Resp:
    return Resp(file_page)


@pytest.fixture
def resp_cancel(base_path, file_page) -> RespCancel:
    return RespCancel(file_page)


@pytest.fixture
def resp_text(base_path, file_page) -> RespText:
    return RespText(file_page)
