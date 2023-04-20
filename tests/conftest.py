import os

import aiofiles
import pytest

from tests.data.data import control_value
from tests.fixtures import Resp, RespCancel, RespText


@pytest.fixture()
def base_path() -> str:
    return os.path.dirname(os.path.abspath(__name__))


@pytest.fixture()
def file_page_2(base_path: str):
    if base_path.split("/")[-1] == "tests":
        return os.path.join(base_path, "data/git_s.html")
    return os.path.join(base_path, "tests/data/git_s.html")


@pytest.fixture()
def file_page(base_path: str):
    if base_path.split("/")[-1] == "tests":
        return os.path.join(
            os.path.dirname(os.path.abspath(__name__)), "data/test.html"
        )
    return os.path.join(
        os.path.dirname(os.path.abspath(__name__)), "tests/data/test.html"
    )


@pytest.fixture()
async def page_2(file_page_2: str) -> str:
    async with aiofiles.open(file_page_2, "r") as file:
        return await file.read()


@pytest.fixture()
async def page(file_page: str) -> str:
    async with aiofiles.open(file_page, "r") as file:
        return await file.read()


@pytest.fixture()
def resp_text(base_path: str, file_page: str) -> RespText:
    return RespText(file_page)


@pytest.fixture()
def download_folder(base_path: str):
    if base_path.split("/")[-1] == "tests":
        return os.path.join(base_path, "download")
    return os.path.join(base_path, "tests/download")


@pytest.fixture()
def resp(base_path: str, file_page: str) -> Resp:
    return Resp(file_page)


@pytest.fixture()
def control_href_value():
    return control_value


@pytest.fixture()
def file_test(base_path: str):
    if base_path.split("/")[-1] == "tests":
        return os.path.join(base_path, "data/master.zip")
    return os.path.join(base_path, "tests/data/master.zip")


@pytest.fixture()
def url1():
    return "https://github.com/VIVERA83?tab=repositories"


@pytest.fixture()
def url2():
    return "https://github.com/VIVERA83/game_sapper"


@pytest.fixture()
def resp_cancel(base_path: str, file_page: str) -> RespCancel:
    return RespCancel(file_page)
