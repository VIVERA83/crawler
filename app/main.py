"""
Модуль запуска приложения
"""
import asyncio
import logging

from core.crawler import Crawler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    ru = [
        ["tbody", "a", {"href", "title"}],
        ["div", "a", {"download", "href"}],
    ]
    URL = "https://gitea.radium.group/" "radium/project-configuration/"
    crawler = Crawler(url=URL, rules=ru, count_worker=3)
    try:
        print(*asyncio.run(crawler.get_result(), debug=True), sep="\n")
    except KeyboardInterrupt:
        logging.warning(" KeyboardInterrupt")
