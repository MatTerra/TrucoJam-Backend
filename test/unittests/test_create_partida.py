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
        with raises(GameNotReadyException):
            game.create_partida()

    @staticmethod
    def test_create_partida_in_not_full_game_should_raise(
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
