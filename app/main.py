"""
Модуль запуска приложения
"""
import asyncio
import logging

from icecream import ic

from app.core.crawler import Crawler

logging.basicConfig(level=logging.INFO)
result = []

# rules = [["tbody", "a", {"href", "title"}], ["div", "a", {"download", "href"}]]  # noqa
# URL = "https://gitea.radium.group/radium/project-configuration/"

rules = [["turbo-frame", "a", {"href", "itemprop"}],
         ["tab-container", "a",
          {"class", "rel", "data-hydro-click", "data-ga-click", "data-hydro-click-hmac", "data-open-app", "data-turbo",
           "href"}
]
         ]  # noqa
# URL = "https://github.com/VIVERA83?tab=repositories"
URL = "https://github.com/VIVERA83/crawler"
# URL = "https://github.com/VIVERA83/game_sapper"
if __name__ == "__main__":
    crawler = Crawler(url=URL, rules=rules, count_worker=3)
    try:
        result = asyncio.run(crawler.get_result(), debug=True)
        ic(crawler.visited)
    except KeyboardInterrupt:
        logging.warning(" KeyboardInterrupt")
    print(*result, sep="\n")
