import os
import shutil

import pytest

from tests.data.data import content, control_value


@pytest.fixture
def url1():
    return "https://github.com/VIVERA83?tab=repositories"


@pytest.fixture
def url2():
    return "https://github.com/VIVERA83/game_sapper"


@pytest.fixture
def base_path() -> str:
    return os.path.dirname(os.path.abspath(__name__))


@pytest.fixture
def file_test(base_path):
    if base_path.split('/')[-1] == "tests":
        return os.path.join(base_path, "data/master.zip")
    return os.path.join(base_path, "tests/data/master.zip")


@pytest.fixture
def file_page(base_path):
    if base_path.split('/')[-1] == "tests":
        return os.path.join(base_path, "data/test.html")
    return os.path.join(base_path, "tests/data/master.zip")


@pytest.fixture
def download_folder(base_path):
    if base_path.split('/')[-1] == "tests":
        return os.path.join(base_path, "download/test")
    return os.path.join(base_path, "tests/download/test")


@pytest.fixture
def page():
    return content


@pytest.fixture
def control_href_value():
    return control_value


@pytest.fixture(autouse=True, scope="function")
def clear(download_folder):
    if os.path.exists(download_folder):
        shutil.rmtree(download_folder)
    yield
    if os.path.exists(download_folder):
        shutil.rmtree(download_folder)

