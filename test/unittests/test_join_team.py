from unittest.mock import Mock
from copy import deepcopy
from pytest import mark, raises

from nova_api import dao

from utils.controller import game_api
from utils.entity.game import Game, GameStatus
from test.unittests import *
from utils.exceptions.invalid_team_exception import InvalidTeamException
from utils.exceptions.user_already_in_game_exception import \
    UserAlreadyInGameException
from utils.exceptions.wrong_password_exception import WrongPasswordException


class TestJoinTeam():
    @staticmethod
    @mark.parametrize("team", [
        -1, 2, 3, "1"
    ])
    def test_join_team_not_0_1_should_raise(team, game_with_players):
        with raises(InvalidTeamException):
            game_with_players.join_team(id_, team)

    @staticmethod
    @mark.parametrize("team", [
        0, 1
    ])
    def test_join_team_should_add_to_team(team, game_with_players):
        game_with_players.join_team("computer1", team)
        assert "computer1" in game_with_players.times[team]

    @staticmethod
    def test_join_team_may_change_team(game_with_players):
        game_with_players.join_team(id_, 0)
        assert id_ in game_with_players.times[0]
        game_with_players.join_team(id_, 1)
        assert id_ not in game_with_players.times[0]
        assert id_ in game_with_players.times[1]

    @staticmethod
    def test_join_team_computer(game_with_players):
        game_with_players.jogadores = [id_, TOKEN_INFO.get("sub")]
        game_with_players.join_team_bot(id_, 0)
        assert "computer1" in game_with_players.times[0]
        game_with_players.join_team_bot(id_, 1)
        assert "computer2" in game_with_players.times[1]
        assert game_with_players.status == GameStatus.Pronto
        game_with_players.remove_team_bot(id_, 0)
        assert "computer1" in game_with_players.times[1]
        assert "computer2" not in game_with_players.times[0]
        assert game_with_players.status == GameStatus.AguardandoJogadores
