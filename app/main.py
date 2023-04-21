"""Модуль запуска приложения"""
import asyncio
import logging

from app.core.crawler import Crawler

logging.basicConfig(level=logging.INFO)
rules = [
    ["tbody", "a", {"href", "title"}],
    ["div", "a", {"download", "href"}],
]
url = "https://gitea.radium.group/" "radium/project-configuration/"


async def main() -> list[str]:
    """Функция запуска приложения"""
    crawler = Crawler(url=url, rules=rules, count_worker=3)
    return await crawler.get_result()


if __name__ == "__main__":  # pragma: no cover
    try:
        print(*asyncio.run(main()), sep="\n")
    except KeyboardInterrupt:
        logging.warning(" KeyboardInterrupt")
