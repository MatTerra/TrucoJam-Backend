from pytest import fixture

from utils.entity.game import Game
from utils.entity.partida import Partida
from test.unittests import *


class TestGames:
    def test_game1(self):
        partida = Partida(**{
            "maos": [
                {
                    "cartas": [
                        {
                            "naipe": 2,
                            "rodada": 2,
                            "valor": 6
                        },
                        {
                            "naipe": 3,
                            "rodada": None,
                            "valor": 7
                        },
                        {
                            "naipe": 3,
                            "rodada": 1,
                            "valor": 4
                        }
                    ],
                    "jogador": TOKEN_INFO.get("sub")
                },
                {
                    "cartas": [
                        {
                            "naipe": 0,
                            "rodada": 1,
                            "valor": 4
                        },
                        {
                            "naipe": 0,
                            "rodada": 2,
                            "valor": 5
                        },
                        {
                            "naipe": 0,
                            "rodada": None,
                            "valor": 1
                        }
                    ],
                    "jogador": "computer2"
                },
                {
                    "cartas": [
                        {
                            "naipe": 3,
                            "rodada": 1,
                            "valor": 6
                        },
                        {
                            "naipe": 3,
                            "rodada": 2,
                            "valor": 2
                        },
                        {
                            "naipe": 1,
                            "rodada": None,
                            "valor": 5
                        }
                    ],
                    "jogador": "computer1"
                },
                {
                    "cartas": [
                        {
                            "naipe": 0,
                            "rodada": 1,
                            "valor": 2
                        },
                        {
                            "naipe": 2,
                            "rodada": 2,
                            "valor": 7
                        },
                        {
                            "naipe": 1,
                            "rodada": None,
                            "valor": 7
                        }
                    ],
                    "jogador": "computer3"
                }
            ],
            "may_raise": [
                True,
                True
            ],
            "turno": 3,
            "valor": 1,
            "vencedor": None
        })
        game = Game(jogadores=[TOKEN_INFO.get("sub"), "computer1",
                               "computer2", "computer3"],
                    partidas=[dict(partida)],
                    times=[[TOKEN_INFO.get("sub"), "computer1"],
                           ["computer2", "computer3"]])
        print(partida.get_round_winner(1))
        print(partida.get_round_winner(2))
        game.check_partida_winner(partida)
        assert partida.vencedor is None
