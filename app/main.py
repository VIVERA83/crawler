"""
Модуль запуска приложения
"""
import asyncio
import logging

from app.core.crawler import Crawler

logging.basicConfig(level=logging.INFO)
result = []

# rules = [["tbody", "a", {"href", "title"}], ["div", "a", {"download", "href"}]]  # noqa
# URL = "https://gitea.radium.group/radium/project-configuration/"

rules = [["turbo-frame", "a", {"href", "itemprop"}]]  # noqa
URL = "https://github.com/VIVERA83?tab=repositories"

if __name__ == "__main__":
    crawler = Crawler(url=URL, rules=rules, count_worker=3)
    try:
        result = asyncio.run(crawler.get_result(), debug=True)
    except KeyboardInterrupt:
        logging.warning(" KeyboardInterrupt")
    print(*result, sep="\n")
