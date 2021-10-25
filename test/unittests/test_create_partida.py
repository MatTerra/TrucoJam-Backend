from pytest import raises

from test.unittests import *
from utils.entity.game import GameStatus
from utils.entity.partida import Partida
from utils.exceptions.game_not_ready_exception import GameNotReadyException
from utils.exceptions.game_over_exception import GameOverException
from utils.exceptions.partida_ongoing_exception import PartidaOngoingException


class TestCreatePartida:
    @staticmethod
    def test_create_partida_in_game_with_ongoing_partida_should_raise(
            game_with_players_and_hands
    ):
        with raises(PartidaOngoingException):
            game_with_players_and_hands.create_partida(id_)

    @staticmethod
    def test_create_partida_in_ended_game_should_raise(
            game_with_players
    ):
        game_with_players.status = GameStatus.Encerrado
        with raises(GameOverException):
            game_with_players.create_partida(id_)

    @staticmethod
    def test_create_partida_in_not_full_game_should_raise(
            game
    ):
        game.join(id_, game.senha)
        with raises(GameNotReadyException):
            game.create_partida(id_)

    @staticmethod
    def test_create_partida_game_with_human_not_in_team_should_raise(
            game_with_players_and_hands
    ):
        game_with_players_and_hands.times = [[id_], []]
        game_with_players_and_hands.partidas = []
        with raises(GameNotReadyException):
            game_with_players_and_hands.create_partida(id_)

    @staticmethod
    def test_create_partida(
            game_with_players_and_hands
    ):
        game_with_players_and_hands.times = [[id_, "computer1"], [TOKEN_INFO.get("sub"), "computer2"]]
        game_with_players_and_hands.partidas = []
        game_with_players_and_hands.create_partida(id_)
        partida = Partida(**game_with_players_and_hands.partidas[0])
        assert len(partida.maos) == 4
        assert partida.turno == 0
        assert partida.valor == 1
        assert partida.vencedor is None
        for mao in partida.maos:
            assert mao["jogador"]
            assert len(mao["cartas"]) == 3
            for card in mao["cartas"]:
                assert card["rodada"] is None

    @staticmethod
    def test_create_with_mixed_order(game_with_players_and_hands):
        player_id_ = TOKEN_INFO.get("sub")
        game_with_players_and_hands.times = [
            [player_id_, "computer2"], [id_, "computer1"]
        ]
        game_with_players_and_hands.partidas = []
        game_with_players_and_hands.create_partida(id_)
        partida = Partida(**game_with_players_and_hands.partidas[0])
        assert partida.maos[0]["jogador"] == player_id_
        assert partida.maos[1]["jogador"] == id_
        assert partida.maos[2]["jogador"] == "computer2"
        assert partida.maos[3]["jogador"] == "computer1"
