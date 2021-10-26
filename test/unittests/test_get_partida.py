from pytest import raises

from test.unittests import *
from utils.entity.card import Suit, Value
from utils.entity.partida import Partida
from utils.entity.game import GameStatus
from utils.exceptions.game_over_exception import GameOverException
from utils.exceptions.user_not_in_game_exception import UserNotInGameException


class TestGetPartida:
    @staticmethod
    def test_get_partida_should_return_none_if_no_partidas(game_with_players):
        assert game_with_players.get_current_partida("computer1") is None

    @staticmethod
    def test_get_game_with_partida_should_return_partida(game_with_players):
        p = Partida()
        game_with_players.partidas = [dict(p)]

        assert game_with_players.get_current_partida("computer1") == p

    @staticmethod
    def test_get_game_with_partida_with_hand_should_exclude_adversary(
            game_with_players, partida_with_hands):
        game_with_players.partidas = [dict(partida_with_hands)]

        partida_with_hands.maos = [mao_id_]

        partida = game_with_players.get_current_partida(id_)
        assert partida.maos == [mao_id_]
        assert partida == partida_with_hands

    @staticmethod
    def test_get_partida_game_over_should_raise(game_with_players):
        game_with_players.status = GameStatus.Encerrado

        with raises(GameOverException):
            game_with_players.get_current_partida(id_)

    @staticmethod
    def test_get_game_with_partida_with_hand_should_include_played_cards(
            game_with_players, partida_with_hands):
        partida_with_hands.maos[1]["cartas"][0]["rodada"] = 1
        partida_with_hands.maos[2]["cartas"][0]["rodada"] = 1

        game_with_players.partidas = [dict(partida_with_hands)]

        partida_with_hands.maos = [
            mao_id_,
            {
                "jogador": TOKEN_INFO.get("sub"),
                "cartas": [
                    {
                        "naipe": Suit.COPAS.value,
                        "valor": Value.ACE.value,
                        "rodada": 1
                    }
                ]
            },
            {
                "jogador": "computer1",
                "cartas": [
                    {
                        "naipe": Suit.ESPADAS.value,
                        "valor": Value.MANILHA.value,
                        "rodada": 1
                    }
                ]
            }
        ]

        partida = game_with_players.get_current_partida(id_)
        assert partida.maos == [mao_id_,
                                {
                                    "jogador": TOKEN_INFO.get("sub"),
                                    "cartas": [
                                        {
                                            "naipe": Suit.COPAS.value,
                                            "valor": Value.ACE.value,
                                            "rodada": 1
                                        }
                                    ]
                                },
                                {
                                    "jogador": "computer1",
                                    "cartas": [
                                        {
                                            "naipe": Suit.ESPADAS.value,
                                            "valor": Value.MANILHA.value,
                                            "rodada": 1
                                        }
                                    ]
                                }
                                ]
        assert partida == partida_with_hands

    @staticmethod
    def test_should_raise_user_not_in_game(game_with_players):
        with raises(UserNotInGameException):
            game_with_players.get_current_partida("computer3")
