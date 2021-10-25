import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock

from pytest import fixture

from utils.entity.card import Suit, Value
from utils.entity.game import Game
from utils.entity.partida import Partida

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

id_="ee81aa59cf1b41ea979e51f5170a128b"
team_id_="0"

mao_id_ = {
    "jogador": id_,
    "cartas": [
        {
            "naipe": Suit.COPAS.value,
            "valor": Value.MANILHA.value,
            "rodada": None
        },
        {
            "naipe": Suit.OUROS.value,
            "valor": Value.KING.value,
            "rodada": None
        },
        {
            "naipe": Suit.OUROS.value,
            "valor": Value.JACK.value,
            "rodada": None
        }
    ]
}


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


__all__=["dao_mock", "success_response", "error_response",
         "TOKEN_INFO", "game", "id_", "team_id_"]
@fixture
def game_with_players():
    game = Game()
    game.join(id_)
    game.join(TOKEN_INFO["sub"])
    game.join("computer1")
    game.join("computer2")
    return game


@fixture
def game_with_players_and_hands(partida_with_hands):
    game = Game()
    game.join(id_)
    game.join("computer2")
    game.join("computer1")
    game.join(TOKEN_INFO["sub"])
    game.times = [[id_, "computer1"], [TOKEN_INFO.get("sub"), "computer2"]]
    game.partidas = [dict(partida_with_hands)]
    return game

@fixture()
def partida_with_hands():
    maos = [
        mao_id_,
        {
            "jogador": TOKEN_INFO.get("sub"),
            "cartas": [
                {
                    "naipe": Suit.COPAS.value,
                    "valor": Value.ACE.value,
                    "rodada": None
                },
                {
                    "naipe": Suit.OUROS.value,
                    "valor": Value.ACE.value,
                    "rodada": None
                },
                {
                    "naipe": Suit.ESPADAS.value,
                    "valor": Value.MANILHA.value,
                    "rodada": None
                }
            ]
        },
        {
            "jogador": "computer1",
            "cartas": [
                {
                    "naipe": Suit.ESPADAS.value,
                    "valor": Value.MANILHA.value,
                    "rodada": None
                },
                {
                    "naipe": Suit.ESPADAS.value,
                    "valor": Value.QUEEN.value,
                    "rodada": None
                },
                {
                    "naipe": Suit.PAUS.value,
                    "valor": Value.QUEEN.value,
                    "rodada": None
                }
            ]
        },
        {
            "jogador": "computer2",
            "cartas": [
                {
                    "naipe": Suit.PAUS.value,
                    "valor": Value.MANILHA.value,
                    "rodada": None
                },
                {
                    "naipe": Suit.PAUS.value,
                    "valor": Value.THREE.value,
                    "rodada": None
                },
                {
                    "naipe": Suit.OUROS.value,
                    "valor": Value.THREE.value,
                    "rodada": None
                }
            ]
        }
    ]

    return Partida(maos=maos)


__all__ = ["dao_mock", "success_response", "error_response",
           "TOKEN_INFO", "game", "id_", "game_with_players",
           "game_with_players_and_hands", "mao_id_",
           "partida_with_hands"]
