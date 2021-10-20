import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock

from pytest import fixture

from utils.entity.game import Game

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(
    str(Path(os.path.join(script_dir, "..", "..", "src")).resolve()))

TOKEN_INFO = {
    "iat": datetime.now().timestamp(),
    "exp": (datetime.now() + timedelta(1.0)).timestamp(),
    "iss": "https://securetoken.google.com/trucojam",
    "aud": "trucojam",
    "sub": "23f2f1750af74f4b8d38683e4ed1b80b"
}

id_ = "ee81aa59cf1b41ea979e51f5170a128b"


@fixture
def dao_mock():
    dao_mock = Mock()
    dao_mock.get_all.return_value = 0, []
    return dao_mock


@fixture(autouse=True)
def success_response(mocker):
    mock = mocker.patch("utils.controller.game_api.success_response")
    mock.side_effect = lambda status_code=200, message="OK", data={}: \
        (status_code, message, data)
    return mock


@fixture(autouse=True)
def error_response(mocker):
    mock = mocker.patch("utils.controller.game_api.error_response")
    mock.side_effect = lambda status_code=500, message="Error", data={}: \
        (status_code, message, data)
    return mock


@fixture
def game():
    return Game(id_=id_, senha="123")


__all__ = ["dao_mock", "success_response", "error_response",
           "TOKEN_INFO", "game", "id_"]
