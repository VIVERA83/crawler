import asyncio

import aiofiles
from aiohttp import ClientResponse


class Resp(ClientResponse):
    def __init__(self, file_path):  # noqa
        self.file_path = file_path

    async def read(self: "Resp") -> bytes:
        async with aiofiles.open(self.file_path, "rb") as file:
            return await file.read()


class RespCancel(Resp):
    async def read(self: "RespCancel"):
        """Имитация Response.read"""
        await asyncio.sleep(3)


class RespText(Resp):
    text = b"Hello world!"

    async def read(self: "RespText") -> bytes:
        """Имитация Response.read"""
        return self.text

    @property
    def len(self: "RespText") -> int:
        """
        Размер файла
        """
        return len(self.text)

    @property
    def content_type(self: "RespText") -> str:
        return "text/html"
