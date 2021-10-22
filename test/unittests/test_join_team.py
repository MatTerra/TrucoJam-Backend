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

# class TestJoinTeam():
#     @staticmethod
#     def test_Should_Return_403_if_team_doesnt_exist(dao_mock,game,):
#         team_id_ = 3
#         dao_mock.get.return_value = game
#         res = game_api.join_team.__wrapped__(id_=id_,
#                                         team_id_= team_id_,
#                                         token_info=TOKEN_INFO,
#                                         dao=dao_mock)
#
#
#         assert res == (412, "This team doesn't exist", {"team_id_": team_id_})
#         dao_mock.update.assert_not_called()