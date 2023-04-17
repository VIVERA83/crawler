# import asyncio
# import os
# from typing import Optional
#
# import aiofiles
# from aiohttp import ClientResponse
# from pip._internal.models.link import Link
#
# from core.data_classes import LinkA
# from core.schema import LinkASchema
# from core.utils import check_attrs, get_links, download_file
# from tests.data.data import content
#
# if __name__ == "__main__":
#     from icecream import ic
#     from bs4 import BeautifulSoup, Tag
#
#     """
#     links = get_links(content, "turbo-frame", "a", {"href", "itemprop"})
#     ic(links)
#     assert len(links) == 9
#     assert isinstance(links, set)
#     control_href_value = [
#         "/VIVERA83/KTS_WINTER_4",
#         "/VIVERA83/Sprint_7",
#         "/VIVERA83/VIVERA83",
#         "/VIVERA83/some_api_service",
#         "/VIVERA83/CardHolderClient",
#         "/VIVERA83/Codewars",
#         "/VIVERA83/game_sapper",
#         "/VIVERA83/CardHolder",
#         "/VIVERA83/test_math_for_kids",
#     ]
#     for link in links:
#         assert link.href in control_href_value, ic(link.href)
#
#     # for i in soup.find_all(lambda t):
#     # url = "https://github.com/VIVERA83/crawler"
#     # ic(URL(url).create_url("/crawler"))
#     # "div", "a",                                                        {"class", "title", "data-turbo-frame", "href"}
#     """
#
#     base_path = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))
#
#
#     class Resp(ClientResponse):
#         def __init__(self):  # noqa
#             pass
#
#         async def read(self) -> bytes:
#             file_path = os.path.join(base_path, "data/test.html")
#             ic(base_path)
#             async with aiofiles.open(file_path, "rb") as f:
#                 return await f.read()
#
#
#     resp = Resp()
#
#     asyncio.run(download_file(resp, "test_2.html", base_path))
