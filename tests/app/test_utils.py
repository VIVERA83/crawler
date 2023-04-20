import asyncio
import hashlib
import os
from typing import List

import aiofiles

from app.core.utils import (
    URL,
    create_folder,
    download_file,
    get_hash_sha256,
    get_links,
)


class TestURL:
    def test_create_url(self: "TestURL", url1: str, url2: str):
        """
        Проверка на корректное создание url ссылки
        :return:
        """
        path = "/VIVERA83/game_sapper"

        assert URL(url1).create_url(path) == url2

    def test_get_url(self: "TestURL", url1: str):
        """
        Проверка на то чно вернется корректный базовой url адрес,
        по которому был инициализирован объект
        :return:
        """
        assert URL(url1).get_url == url1

    def test_get_uri(self: "TestURL", url1: str, url2: str):
        """
        Проверка на то что uri ссылка корректно возвращается
        :param url1:
        :param url2:
        :return:
        """
        uri1 = "/VIVERA83?tab=repositories"
        uri2 = "/VIVERA83/game_sapper"
        assert URL(url1).get_uri == uri1
        assert URL(url2).get_uri == uri2


class TestGetHashSha256:
    async def test_get_hash_sha256(self: "TestGetHashSha256", file_test: str):
        """
        Проверка на корректный возврат hash файла
        :return:
        """
        hsh = hashlib.sha256()
        with open(file_test, "rb") as file:
            hsh.update(file.read())
        assert hsh.hexdigest() == await get_hash_sha256(file_test)


class TestCheckAttrs:
    def test_check_and_get_links(
        self: "TestCheckAttrs", page: str, control_href_value: List[str]
    ):
        """Проверка корректной работы check_attrs и get_links"""
        links = get_links(page, "turbo-frame", "a", {"href", "itemprop"})
        assert isinstance(links, set)
        assert len(links) == 9
        for link in links:
            assert link.href in control_href_value


class TestCreateFolder:
    def test_create_folder(self: "TestCreateFolder", download_folder: str):
        """
        Проверим создание вложенных папок
        """
        new_folder = "test1"
        assert os.path.join(download_folder, new_folder) == create_folder(
            download_folder, new_folder
        )


class TestDownloadFile:
    """
    Проверка на скачивание, и корректное сохранение
    """

    async def test_download_binary_file(
        self: "TestDownloadFile",
        resp: str,
        base_path: str,
        file_page: str,
        download_folder: str,
    ):
        filename = await download_file(resp, file_page, download_folder)
        async with aiofiles.open(filename, "br") as file:
            async with aiofiles.open(file_page, "br") as file_2:
                assert len(await file.read()) == len(await file_2.read())

    async def test_download_text_file(
        self: "TestDownloadFile",
        resp_text: str,
        base_path: str,
        file_page: str,
        download_folder: str,
    ):
        filename = await download_file(
            resp=resp_text,
            path=file_page,
            download_folder=download_folder,
            mode="w",
            logger=None,
        )
        async with aiofiles.open(filename) as file:
            assert len(await file.read()) == resp_text.len

    async def test_cancel_download(
        self: "TestDownloadFile",
        resp_cancel: str,
        base_path: str,
        file_page: str,
        download_folder: str,
    ):
        """
        Проверка на корректную работу при прерывании процесса закачки файла
        """

        assert not await asyncio.wait_for(
            download_file(resp_cancel, "m.zip", base_path), 1
        )
