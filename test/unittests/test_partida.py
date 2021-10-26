from pytest import raises, mark

from test.unittests import *
from utils.exceptions.card_already_played_exception import \
    CardAlreadyPlayedException
from utils.exceptions.invalid_card_exception import InvalidCardException
from utils.exceptions.not_user_turn_exception import NotUserTurnException
from utils.exceptions.partida_over_exception import PartidaOverException


class TestPartida:
    @staticmethod
    def test_play_card_out_of_turn_should_raise(partida_with_hands):
        with raises(NotUserTurnException):
            partida_with_hands.play(1, 0)

    @staticmethod
    def test_play_card_already_played_should_raise(partida_with_hands):
        partida_with_hands.maos[0]["cartas"][0]["rodada"] = 1
        with raises(CardAlreadyPlayedException):
            partida_with_hands.play(0, 0)

        partida_with_hands.maos[0]["cartas"][0]["rodada"] = None

    @staticmethod
    @mark.parametrize("card", [
        -1, 3, 5
    ])
    def test_play_invalid_card_should_raise(partida_with_hands, card):
        with raises(InvalidCardException):
            partida_with_hands.play(0, card)

    @staticmethod
    def test_play_card_should_play(partida_with_hands):
        partida_with_hands.play(0, 0)

        assert partida_with_hands.maos[0]["cartas"][0]["rodada"] == 1
        partida_with_hands.maos[0]["cartas"][0]["rodada"] = None

    @staticmethod
    def test_play_card_should_increment_turn(partida_with_hands):
        partida_with_hands.play(0, 0)

        assert partida_with_hands.turno == 1
        partida_with_hands.maos[0]["cartas"][0]["rodada"] = None
        partida_with_hands.turno = 0

    @staticmethod
    def test_turn_should_wrap_at_end(partida_with_hands):
        partida_with_hands.play(0, 0)
        partida_with_hands.play(1, 0)
        partida_with_hands.play(2, 0)
        partida_with_hands.play(3, 1)

        partida_with_hands.play(0, 1)
        assert partida_with_hands.turno == 1
        TestPartida.reset_partida(partida_with_hands)
        partida_with_hands.turno = 0

    @staticmethod
    def test_round_should_be_incremented(partida_with_hands):
        TestPartida.reset_partida(partida_with_hands)
        partida_with_hands.play(0, 0)
        partida_with_hands.play(1, 0)
        partida_with_hands.play(2, 0)
        partida_with_hands.play(3, 1)
        partida_with_hands.play(0, 1)

        assert partida_with_hands.maos[0]["cartas"][0]["rodada"] == 1
        assert partida_with_hands.maos[1]["cartas"][0]["rodada"] == 1
        assert partida_with_hands.maos[2]["cartas"][0]["rodada"] == 1
        assert partida_with_hands.maos[3]["cartas"][1]["rodada"] == 1
        assert partida_with_hands.maos[0]["cartas"][1]["rodada"] == 2
        TestPartida.reset_partida(partida_with_hands)

    @staticmethod
    def test_play_on_partida_won_should_raise(partida_with_hands):
        TestPartida.reset_partida(partida_with_hands)
        partida_with_hands.play(0, 0)
        partida_with_hands.play(1, 0)
        partida_with_hands.play(2, 0)
        partida_with_hands.play(3, 0)

        assert partida_with_hands.turno == 3

        partida_with_hands.play(3, 1)
        partida_with_hands.play(0, 1)
        partida_with_hands.play(1, 1)
        partida_with_hands.play(2, 1)
        partida_with_hands.vencedor = 1

        with raises(PartidaOverException):
            partida_with_hands.play(3, 2)

    @staticmethod
    def test_turn_should_be_to_round_winner(partida_with_hands):
        TestPartida.reset_partida(partida_with_hands)
        partida_with_hands.play(0, 0)
        partida_with_hands.play(1, 0)
        partida_with_hands.play(2, 0)

        assert partida_with_hands.maos[0]["cartas"][0]["rodada"] == 1
        assert partida_with_hands.maos[1]["cartas"][0]["rodada"] == 1
        assert partida_with_hands.maos[2]["cartas"][0]["rodada"] == 1

        partida_with_hands.play(3, 0)
        assert partida_with_hands.turno == 3

    @staticmethod
    def reset_partida(partida_with_hands):
        for i in range(4):
            for j in range(3):
                partida_with_hands.maos[i]["cartas"][j]["rodada"] = None
        partida_with_hands.turno = 0
