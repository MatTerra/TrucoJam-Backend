from datetime import datetime, timedelta
from typing import Type
from unittest.mock import Mock

from pytest import fixture, raises

from utils.controller import game_api
from utils.entity.game import Game
from test.unittests import dao_mock, success_response, TOKEN_INFO, game


def raise_exception(exc_type: Type[Exception] = Exception):
    raise exc_type()


class TestGameAPI:
    @staticmethod
    def test_probe_ok(dao_mock):
        res = game_api.probe.__wrapped__(dao_mock)
        assert res == (200, "API Ready", {"available": 0})

    @staticmethod
    def test_probe_not_ok(dao_mock):
        dao_mock.get_all.side_effect = raise_exception
        with raises(Exception):
            game_api.probe.__wrapped__(dao_mock)

    @staticmethod
    def test_read_empty(dao_mock):
        res = game_api.read.__wrapped__(
            dao=dao_mock,
            token_info=TOKEN_INFO)
        assert res == (200, "List of game", {"total": 0, "results": []})

    @staticmethod
    def test_read_with_one(dao_mock: Mock, game: Game):
        dao_mock.get_all.return_value = 1, [game]
        res = game_api.read.__wrapped__(
            dao=dao_mock,
            token_info=TOKEN_INFO)
        assert res == (200, "List of game", {"total": 1, "results": [
            dict(game)
        ]})
        dao_mock.get_all.assert_called_with(length=20, offset=0, filters=None)

    @staticmethod
    def test_read_with_limit(dao_mock: Mock, game: Game):
        dao_mock.get_all.return_value = 1, [game]
        res = game_api.read.__wrapped__(
            length=2, dao=dao_mock, token_info=TOKEN_INFO)
        assert res == (200, "List of game", {"total": 1, "results": [
            dict(game)
        ]})
        dao_mock.get_all.assert_called_with(length=2, offset=0, filters=None)

    @staticmethod
    def test_read_with_offset(dao_mock: Mock, game: Game):
        dao_mock.get_all.return_value = 3, [game]
        res = game_api.read.__wrapped__(
            offset=2, dao=dao_mock,
            token_info=TOKEN_INFO)
        assert res == (200, "List of game", {"total": 3, "results": [
            dict(game)
        ]})
        dao_mock.get_all.assert_called_with(length=20, offset=2, filters=None)

    @staticmethod
    def test_read_one_found(dao_mock: Mock, game: Game):
        dao_mock.get.return_value = game

        res = game_api.read_one.__wrapped__(id_=game.id_, dao=dao_mock,
                                            token_info=TOKEN_INFO)

        dao_mock.get.assert_called_with(id_=game.id_)
        assert res == (200, "Game retrieved", {"Game": dict(game)})

    @staticmethod
    def test_read_one_not_found(dao_mock: Mock, game: Game):
        dao_mock.get.return_value = None

        res = game_api.read_one.__wrapped__(id_=game.id_, dao=dao_mock,
                                            token_info=TOKEN_INFO)

        dao_mock.get.assert_called_with(id_=game.id_)
        assert res == (404, "Game not found in database", {"id_": game.id_})

    @staticmethod
    def test_create(dao_mock: Mock, game: Game):
        res = game_api.create.__wrapped__(dict(game), dao_mock,
                                          token_info=TOKEN_INFO)

        assert TOKEN_INFO["sub"] in game.jogadores
        dao_mock.create.assert_called_with(entity=game)
        assert res == (201, "Game created", {"Game": dict(game)})
