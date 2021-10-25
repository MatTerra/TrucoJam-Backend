from uuid import uuid4

from pytest import raises

from test.unittests import *
from utils.exceptions.user_not_in_game_exception import UserNotInGameException


class TestRaise:
    @staticmethod
    def test_raise_with_user_not_in_game_should_raise(
            game_with_players_and_hands
    ):
        with raises(UserNotInGameException):
            game_with_players_and_hands.raise_game(uuid4().hex)
