"""Модуль в котором реализован Краулер,  для  обхода страницы."""
from __future__ import annotations

import asyncio
import datetime
import logging
import sys
from asyncio import CancelledError, Queue, Semaphore, Task
from http import HTTPStatus

from aiohttp import ClientConnectorError, ClientSession
from core.data_classes import LinkA

from app.core.utils import URL, download_file, get_hash_sha256, get_links

# для совместимости с более ранними версиями Python3.
if sys.version_info.minor >= 9:
    from asyncio import to_thread
else:

    async def to_thread(
        content: str, search_location: str, teg_name: str, attrs: set[str]
    ) -> set[LinkA]:
        """
        Альтернатива asyncio.to_thread для более ранних версий Python3
        :param args:
        :return:
        """
        return await asyncio.get_event_loop().run_in_executor(
            None, get_links, content, search_location, teg_name, attrs
        )


class Crawler:
    """
    Краулер, занимает обкачкой сайта по полученным правилам.
    Правела передаваться в виде списка rules.
    Пример:
    roles = [["tbody", "a", {"href", "title"}],
             ["div", "a", {"download", "href"}]]
    Имеется два правела, по которым выбирается
    ссылка для дальнейшего посещения
        1. ["tbody",  # Тег в котором будем искать.
            "a", # Искомый тег
            {"href", "title"}] # описание параметров
            которые должны быть у тега,

    """

    links: Queue[str] | None = None
    pages: Queue[str] | None = None
    # ограничитель для одновременной работы не более чем указанно в семафоре
    semaphore: Semaphore | None = None
    session: ClientSession | None = None
    counter: int | None = None
    download_folder: str | None = "downloads"
    total_download = 0
    hash_files: list[str] | None = None

    def __init__(
        self: "Crawler",
        url: str,
        rules: list[list[str, str, set[str]]],  #
        count_worker: int = 3,
        count_requests: int = 40,
    ) -> None:
        """

        :param url: Страница для обхода
        :param rules: Правила обхода
        :param count_worker:  Количество воркеров
        :param count_requests: Количество одномоментных запросов к сайту
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.base_url = URL(url)
        self.visited = set()
        self.errors_links = set()
        self.is_running = False
        self.workers: list[Task] | None = []
        self.count_worker = count_worker
        self.count_request = count_requests
        self.rules = rules
        self.logger.info(" Creating crawler:  %s", self.base_url.get_url)

    async def start(self: "Crawler") -> None:
        """
        Метод отвечает за подготовку для начала обкачки сайта
        :return:
        """
        self.links = Queue()
        self.pages = Queue()
        self.links.put_nowait(self.base_url.get_uri)
        self.session = ClientSession()
        self.semaphore = Semaphore(self.count_request)
        self.counter = 1
        self.total_download = 0
        self.hash_files = []
        self.is_running = True
        self.workers = [
            asyncio.create_task(self.worker(name + 1))
            for name in range(self.count_worker)
        ]
        self.workers.append(asyncio.create_task(self.create_links()))
        self.workers.append(asyncio.create_task(self.is_done()))

    async def create_links(self: "Crawler") -> None:
        """
        Метод слушает очередь self.pages, в которой лежать страницы сайта,
        Страницы обкачиваются в отдельном потоке. Из них достаются ссылка для
        обкачки и кладутся в очередь self.links
        :return:
        """
        while self.is_running:
            page = await self.pages.get()
            for rule in self.rules:
                links = await to_thread(get_links, page, *rule)
                for link in links:
                    if not bool(set(link.href) & self.visited):
                        await self.links.put(link.href)
                        self.counter += 1

    async def stop(self: "Crawler") -> None:
        """
        Метод отвечает за корректную остановку краулера
        :return:
        """
        self.is_running = False
        for worker in self.workers:
            if not worker.cancelled():
                worker.cancel()
                await worker
        if not self.session.closed:
            await self.session.close()
        self.logger.debug(" Crawler stopped")

    async def get_result(self: "Crawler") -> list[str]:
        """
        Запускает краулер на выполнение и возвращает список hash
        скаченных файлов.
        1. скаченные файлы помещаются в папку self.download_folder
        2. через лог выводит данные по результатам
        обкачки, начало, окончание и общее время затраченное на обкачку.
        :return:
        """
        await self.start()
        start = datetime.datetime.now()
        self.logger.info(" Started crawler:   %s", start)
        try:
            await asyncio.gather(*self.workers)
        except CancelledError:
            await self.stop()
        stop = datetime.datetime.now()
        self.logger.info(" Stopped crawler:   %s", stop)
        self.logger.info(" Total time works:  %s", stop - start)
        if self.errors_links:
            self.logger.info(" Total error links: %s", len(self.errors_links))
        self.logger.info(" Visited:           %s", len(self.visited))
        self.logger.info(" Total:             %s", self.counter)
        self.logger.info(" Downloaded files:  %s", self.total_download)
        return self.hash_files

    async def is_done(self: "Crawler") -> None:
        """
        Проверяет общее количество ссылок и количеством посещенных,
        если они равны останавливает worker (так как все уже обкачено),
        в противном случае self.links будут работать вечно.

        :return:
        """
        while self.is_running:
            await asyncio.sleep(2)
            is_done = str(self.counter == len(self.visited))
            self.logger.info(
                " Checking:          is_done: "
                "%s"
                " visited: %s total: %s"
                " queue: %s",
                is_done,
                self.visited,
                self.counter,
                self.links.qsize(),
            )
            if self.counter == len(self.visited):
                self.logger.debug(
                    " The queue with links is empty,"
                    " initialization of stopping workers"
                )
                await self.stop()

    async def worker(self: "Crawler", name: int | str = None) -> None:
        """
        Worker, выполняет следующие функции:
        1. Читает из очереди links ссылку и ходит по ссылке
        2. Если ссылка ведет на файл, скачивает файл
        и вычитывает hash_sha256
           hash, сохраняет в self.hash_files
        3. Если ссылка ведет на страницу,
        скаченную страницу кладет в очередь на парсинг.
        Worker, работает пока self.is_running = True
        :param name: Имя Worker, Необязательный параметр
        :return:
        """
        self.logger.debug(" Starting worker: %s", name if name else "")
        while self.is_running:
            try:
                async with self.semaphore:
                    link = await self.links.get()
                    try:
                        async with self.session.get(
                            self.base_url.create_url(link)
                        ) as resp:
                            if resp.status == HTTPStatus.OK:
                                if resp.content_type == "text/html":
                                    page = await resp.text()
                                    await self.pages.put(page)
                                elif resp.content_type == "application/zip":
                                    download_path = await download_file(
                                        resp, link, self.download_folder
                                    )
                                    if download_path:
                                        self.total_download += 1
                                        self.hash_files.append(
                                            await get_hash_sha256(
                                                path_to_file=download_path
                                            )
                                        )
                                elif resp.content_type == "text/plain":
                                    download_path = await download_file(
                                        resp, link, self.download_folder, "w"
                                    )
                                    if download_path:
                                        self.total_download += 1
                                        self.hash_files.append(
                                            await get_hash_sha256(
                                                path_to_file=download_path
                                            )
                                        )
                    except ClientConnectorError as error:
                        self.errors_links.add(link)
                        self.logger.warning("Connection error: %s", link)

                    self.visited.add(link)
                self.logger.debug(" %s : %s", name if name else "Worker", link)
            except CancelledError:
                self.logger.debug(" %s cancelled", name if name else "Worker")
