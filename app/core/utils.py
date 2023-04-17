"""
вспомогательные утилиты, для краулера
"""
import hashlib
import logging
import os
from asyncio import CancelledError
from typing import Optional
from urllib.parse import urlparse

import aiofiles  # pylint: disable= E0401
from aiohttp import ClientResponse
from bs4 import BeautifulSoup, Tag  # pylint: disable= E0401

from app.core.data_classes import LinkA
from app.core.schema import LinkASchema


class URL:
    """Отвечает за формирования url адреса"""

    def __init__(self, url: str):
        self._url = urlparse(url)

    def create_url(self, path: str) -> str:
        """
        Создает на основе полученного path url адрес.
        Пример: https - схема
                gitea.radium.group - домен
                radium/project-configuration - путь
        :param path: Часть url адреса, путь.
        :return:
        """

        return self._url.scheme + "://" + self._url.netloc + path

    @property
    def get_url(self) -> str:
        """
        Возвращает базовый url адрес
        :return:
        """
        return self._url.geturl()

    @property
    def get_uri(self) -> str:
        """
        Возвращает часть url адреса. Путь и параметры.
        :return:
        """
        if self._url.query:
            return self._url.path + "?" + self._url.query
        return self._url.path


async def get_hash_sha256(path_to_file: str) -> str:
    """
    Возвращает хэш сумму по протоколу sha256
    :param path_to_file: Путь к файлу.
    :return:
    """
    hsh = hashlib.sha256()
    async with aiofiles.open(path_to_file, "rb") as file:
        while True:
            data = await file.read(1024)
            if not data:
                return hsh.hexdigest()
            hsh.update(data)


def check_attrs(tag: Tag, tag_name: str, attrs: set[str]) -> Optional[Tag]:
    """
    Проверка тега на соответствие требование по названию и атрибутам
    :param tag: Проверяемы тег.
    :param tag_name: Имя
    :param attrs: атрибуты которые должны присутствовать у тега
    :return:
    """
    if (tag.name == tag_name) and (tag.attrs.keys() == attrs):
        return tag
    return None


def get_links(
    content: str, search_location: str, teg_name: str, attrs: set[str]
) -> set[LinkA]:
    """
    Возвращает список Link тега а, которые находятся в search_location.
    :param content: Html текст в котором производится поиск.
    :param search_location: Тег в котором производится поиск.
    :param teg_name: Тег, который ищем.
    :param attrs: Атрибуты тега которые должны быть.
    :return:
    """
    links = set()
    soup = BeautifulSoup(content, "lxml")
    for tag in soup.find_all(search_location):
        for child in tag.find_all(lambda t: check_attrs(t, teg_name, attrs)):
            links.add(LinkASchema().load(child.attrs))
    return links


def create_folder(download_folder: str, path: str) -> str:
    """
    Создает папку, либо дерево папок согласно переданного пути.
    :param download_folder: Путь до папки сохранения
    :param path: Файл, либо путь внутри папки для сохранения
    :return:
    """
    download_path = os.path.join(download_folder, *path.split("/")[:-1])
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    return os.path.join(download_path, path.split("/")[-1])


async def download_file(
    resp: ClientResponse,
    path: str,
    download_folder: str,
    mode: str = "wb",
    logger: logging.Logger = None,
) -> str:
    """
    Сохраняет файл в указанной папке для сохранения,
    при удачном сохранении возвращает путь к файлу
    :param resp: Response,
    в котором content-type = "application/zip"
    :param path: путь ссылка к файлу,
     по которой будет создаваться дерево каталогов
     для сохранения конечного файла
    :param download_folder: корневая папка в которой сохраняется файл
    :param mode: режим работы с файлом,
     вариация такая же как у обычной функции open
    :param logger: logger
    :return:
    """
    logger = logger or logging.getLogger()
    download_path = create_folder(download_folder, path)
    try:
        async with resp:
            data = await resp.read()
            async with aiofiles.open(file=download_path, mode=mode) as file:  # noqa
                if mode == "w":
                    await file.write(data.decode("utf-8"))
                else:
                    await file.write(data)
            logger.debug(f" Download file:     {download_path}")
            return download_path
    except CancelledError:
        logger.warning(
            "The file download aborted, "
            "the file may be corrupted: %s", download_path
        )
