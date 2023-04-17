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
        await asyncio.sleep(2)


@pytest.fixture
def resp(base_path, file_page) -> ClientResponse:
    return Resp(file_page)


@pytest.fixture
def resp_cancel(base_path, file_page) -> ClientResponse:
    return RespCancel(file_page)
