from uuid import uuid4

from pytest import raises

from test.unittests import *
from utils.entity.game import GameStatus
from utils.exceptions.game_not_ready_exception import GameNotReadyException
from utils.exceptions.game_over_exception import GameOverException
from utils.exceptions.not_user_turn_exception import NotUserTurnException
from utils.exceptions.user_not_in_game_exception import UserNotInGameException


class TestRaise:
    @staticmethod
    def test_raise_with_user_not_in_game_should_raise(
            game_with_players_and_hands
    ):
        with raises(UserNotInGameException):
            game_with_players_and_hands.raise_game(uuid4().hex)

    @staticmethod
    def test_raise_with_status_encerrado_should_raise(
            game_with_players_and_hands
    ):
        game_with_players_and_hands.status = GameStatus.Encerrado
        with raises(GameOverException):
            game_with_players_and_hands.raise_game(TOKEN_INFO.get("sub"))

    @staticmethod
    def test_raise_without_partida_should_raise(game_with_players):
        with raises(GameNotReadyException):
            game_with_players.raise_game(TOKEN_INFO.get("sub"))

    @staticmethod
    def test_raise_out_of_turn_should_raise(game_with_players_and_hands):
        with raises(NotUserTurnException):
            game_with_players_and_hands.raise_game(TOKEN_INFO.get("sub"))

    @staticmethod
    def test_raise_should_raise(game_with_players_and_hands):
        game_with_players_and_hands.raise_game(id_)
        assert game_with_players_and_hands.partidas[0]["valor"] == 3
        assert game_with_players_and_hands.partidas[0]["may_raise"] == [False, True]
