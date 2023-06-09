import os

import pytest

from tests.data.data import control_value


@pytest.fixture()
def base_path() -> str:
    return os.path.dirname(os.path.abspath(__name__))


@pytest.fixture()
def file_test(base_path: str):
    if base_path.split("/")[-1] == "tests":
        return os.path.join(base_path, "data/master.zip")
    return os.path.join(base_path, "tests/data/master.zip")


@pytest.fixture()
def control_href_value():
    return control_value
