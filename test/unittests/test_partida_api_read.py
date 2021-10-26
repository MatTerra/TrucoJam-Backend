from unittest.mock import Mock

from pytest import fixture

from utils.controller import partida_api
from test.unittests import *
from utils.entity.card import Suit, Value
from utils.entity.game import Game


@fixture(autouse=True)
def success_response(mocker):
    mock = mocker.patch("utils.controller.partida_api.success_response")
    mock.side_effect = lambda status_code=200, message="OK", data={}: \
        (status_code, message, data)
    return mock


@fixture(autouse=True)
def error_response(mocker):
    mock = mocker.patch("utils.controller.partida_api.error_response")
    mock.side_effect = lambda status_code=500, message="Error", data={}: \
        (status_code, message, data)
    return mock


class TestPartidaAPIRead:
    @staticmethod
    def test_should_return_partida(dao_mock, game_with_players_and_hands):
        dao_mock.get.return_value = game_with_players_and_hands
        res = partida_api.read.__wrapped__(id_=id_,
                                           token_info={**TOKEN_INFO,
                                                       "sub": id_},
                                           dao=dao_mock)
        dao_mock.get.assert_called_with(id_=id_)
        assert res == (200, "Current partida retrieved",
                       {"partida": {
                           'maos': [mao_id_],
                           'may_raise': [True, True],
                           'turno': 0,
                           'valor': 1,
                           'vencedor': None,
                           "mao_jogador": mao_id_
                       }})

    @staticmethod
    def test_should_return_404_if_game_not_found(dao_mock):
        dao_mock.get.return_value = None
        res = partida_api.read.__wrapped__(id_=id_,
                                           token_info=TOKEN_INFO,
                                           dao=dao_mock)
        dao_mock.get.assert_called_with(id_=id_)
        assert res == (404, "This game doesn't exist", {"id_": id_})

    @staticmethod
    def test_empty_partida_should_return_empty_content(dao_mock):
        game_mock = Mock(Game)
        game_mock.get_current_partida.return_value = None
        dao_mock.get.return_value = game_mock
        res = partida_api.read.__wrapped__(id_=id_,
                                           token_info=TOKEN_INFO,
                                           dao=dao_mock)
        game_mock.get_current_partida.assert_called_with(TOKEN_INFO['sub'])
        assert res == (204, "No current partida", {})


class TestPartidaAPIPlay:
    @staticmethod
    def test_should_return_partida(dao_mock, game_with_players_and_hands):
        for i in range(4):
            for j in range(3):
                game_with_players_and_hands.partidas[0]["maos"] \
                    [i]["cartas"][j]["rodada"] = None
        dao_mock.get.return_value = game_with_players_and_hands
        res = partida_api.play.__wrapped__(id_=id_,
                                           card={"id_": 0},
                                           token_info={**TOKEN_INFO,
                                                       "sub": id_},
                                           dao=dao_mock)
        dao_mock.get.assert_called_with(id_=id_)
        assert res == (200, "Card played",
                       {"partida": {
                           'maos': [{
                               "jogador": id_,
                               "cartas": [
                                   {
                                       "naipe": Suit.COPAS.value,
                                       "valor": Value.MANILHA.value,
                                       "rodada": 1
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
                           }],
                           'may_raise': [True, True],
                           'turno': 1,
                           'valor': 1,
                           'vencedor': None
                       }})

    @staticmethod
    def test_should_return_404_if_game_not_found(dao_mock):
        dao_mock.get.return_value = None
        res = partida_api.play.__wrapped__(id_=id_,
                                           card={"id_": 0},
                                           token_info={**TOKEN_INFO,
                                                       "sub": id_},
                                           dao=dao_mock)
        dao_mock.get.assert_called_with(id_=id_)
        assert res == (404, "This game doesn't exist", {"id_": id_})

    @staticmethod
    def test_empty_partida_should_return_bad_request(dao_mock):
        game_mock = Mock(Game)
        game_mock.get_current_partida.return_value = None
        dao_mock.get.return_value = game_mock
        res = partida_api.play.__wrapped__(id_=id_,
                                           card={"id_": 0},
                                           token_info=TOKEN_INFO,
                                           dao=dao_mock)
        game_mock.get_current_partida.assert_called_with(TOKEN_INFO['sub'])
        assert res == (400, "No current partida", {})
