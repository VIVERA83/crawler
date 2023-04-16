"""
Модуль запуска приложения
"""
import asyncio
import logging

from core.crawler import Crawler

logging.basicConfig(level=logging.INFO)
result = []
rules = [["tbody", "a", {"href", "title"}], ["div", "a", {"download", "href"}]]  # noqa
URL = "https://gitea.radium.group/radium/project-configuration/"

if __name__ == "__main__":
    crawler = Crawler(url=URL, rules=rules, count_worker=3)
    try:
        result = asyncio.run(crawler.get_result(), debug=True)
    except KeyboardInterrupt:
        logging.warning(" KeyboardInterrupt")
    print(*result, sep="\n")
