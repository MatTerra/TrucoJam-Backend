from unittest.mock import Mock
from copy import deepcopy
from pytest import mark, raises

from nova_api import dao

from utils.controller import game_api
from utils.entity.game import Game
from test.unittests import *
from utils.exceptions.user_already_in_game_exception import \
    UserAlreadyInGameException
from utils.exceptions.wrong_password_exception import WrongPasswordException


class TestJoinGame():
    @staticmethod
    def test_join_game_should_return_404_if_game_not_found(dao_mock):
        dao_mock.get.return_value = None
        res = game_api.join.__wrapped__(id_=id_,
                                        password={},
                                        token_info=TOKEN_INFO,
                                        dao=dao_mock)

        dao_mock.get.assert_called_once_with(id_=id_)
        assert res == (404, "This game doesn't exist", {"id_": id_})
        dao_mock.update.assert_not_called()

    @staticmethod
    def test_join_game_should_return_403_if_password_doesnt_match(dao_mock,
                                                                  game):
        dao_mock.get.return_value = game
        with raises(WrongPasswordException):
            game_api.join.__wrapped__(id_=id_,
                                      password={"senha": "outra"},
                                      token_info=TOKEN_INFO,
                                      dao=dao_mock)

        dao_mock.get.assert_called_once_with(id_=id_)
        dao_mock.update.assert_not_called()

    @staticmethod
    def test_join_game_with_password_should_include_player(dao_mock, game):
        dao_mock.get.return_value = game
        res = game_api.join.__wrapped__(id_=id_,
                                        password={"senha": game.senha},
                                        token_info=TOKEN_INFO,
                                        dao=dao_mock)

        assert res == (200, "Joined Game",
                       {"Game": {'id_': 'ee81aa59cf1b41ea979e51f5170a128b',
                                 'creation_datetime': dict(game).get(
                                     "creation_datetime"),
                                 'last_modified_datetime': dict(game).get(
                                     "last_modified_datetime"),
                                 'pontuacao': [0, 0],
                                 'times': [[], []], 'partidas': [],
                                 'jogadores': [TOKEN_INFO["sub"]],
                                 'status': 0}})

        assert TOKEN_INFO['sub'] in game.jogadores

        dao_mock.update.assert_called_with(game)

    @staticmethod
    @mark.parametrize("senha", [
        "1123",
        "abc",
        "",
        None
    ])
    def test_join_game_with_empty_password_should_work_with_any_password(
            dao_mock,
            game, senha):
        game.senha = ""
        dao_mock.get.return_value = game
        res = game_api.join.__wrapped__(id_=id_,
                                        password={"senha": senha},
                                        token_info=TOKEN_INFO,
                                        dao=dao_mock)

        assert res == (200, "Joined Game",
                       {"Game": {'id_': 'ee81aa59cf1b41ea979e51f5170a128b',
                                 'creation_datetime': dict(game).get(
                                     "creation_datetime"),
                                 'last_modified_datetime': dict(game).get(
                                     "last_modified_datetime"),
                                 'pontuacao': [0, 0],
                                 'times': [[], []], 'partidas': [],
                                 'jogadores': [TOKEN_INFO["sub"]],
                                 'status': 0}})

        assert TOKEN_INFO['sub'] in game.jogadores

        dao_mock.update.assert_called_with(game)

    @staticmethod
    def test_join_game_should_return_412_if_user_is_already_in_game(dao_mock,
                                                                    game):
        game.jogadores.append(TOKEN_INFO['sub'])
        dao_mock.get.return_value = game
        with raises(UserAlreadyInGameException):
            game_api.join.__wrapped__(id_=id_,
                                      password={"senha": game.senha},
                                      token_info=TOKEN_INFO,
                                      dao=dao_mock)

        dao_mock.update.assert_not_called()
