import asyncio
import hashlib
import logging
import os
from asyncio import TimeoutError

import aiofiles
import pytest

from app.core.utils import URL, get_hash_sha256, get_links, create_folder, download_file


class TestURL:
    def test_create_url(self, url1, url2):
        """
        Проверка на корректное создание url ссылки
        :return:
        """
        path = "/VIVERA83/game_sapper"

        assert URL(url1).create_url(path) == url2

    def test_get_url(self, url1):
        """
        Проверка на то чно вернется корректный базовой url адрес,
        по которому был инициализирован объект
        :return:
        """
        assert URL(url1).get_url == url1

    def test_get_uri(self, url1, url2):
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
    async def test_get_hash_sha256(self, file_test):
        """
        Проверка на корректный возврат hash файла
        :return:
        """
        hsh = hashlib.sha256()
        with open(file_test, "rb") as file:
            hsh.update(file.read())
        assert hsh.hexdigest() == await get_hash_sha256(file_test)


class TestCheckAttrs:
    def test_check_and_get_links(self, page, control_href_value):
        """Проверка корректной работы check_attrs и get_links"""
        links = get_links(page, "turbo-frame", "a", {"href", "itemprop"})
        assert isinstance(links, set)
        assert len(links) == 9
        for link in links:
            assert link.href in control_href_value, f"Not valid value {link.href}"


class TestCreateFolder:
    def test_create_folder(self, download_folder):
        """
        Проверим создание вложенных папок
        """
        new_folder = "test1"
        assert os.path.join(download_folder, new_folder) == create_folder(download_folder, new_folder)


class TestDownloadFile:
    """
    Проверка на скачивание, и корректное сохранение
    """

    async def test_download_file(self, resp, base_path, file_page):
        filename = await download_file(resp, "download/test_page.html", base_path)
        async with aiofiles.open(filename, "br") as file:
            async with aiofiles.open(file_page, "br") as f:
                assert len(await file.read()) == len(await f.read())

    async def test_cancel_download(self, resp_cancel, base_path, file_page):
        """
        Проверка на корректную работу при прерывании процесса закачки файла
        """
        assert not await asyncio.wait_for(download_file(resp_cancel, "download/test_page.html", base_path), 1)
