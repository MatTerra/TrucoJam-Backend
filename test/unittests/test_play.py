from copy import deepcopy

from pytest import raises

from test.unittests import *
from utils.controller import game_api, partida_api
from utils.entity.game import Game, GameStatus
from utils.entity.partida import Partida
from utils.exceptions.game_over_exception import GameOverException
from utils.exceptions.not_user_turn_exception import NotUserTurnException
from utils.exceptions.user_not_in_game_exception import UserNotInGameException


class TestPlay():
    @staticmethod
    def test_play_should_raise_user_not_in_game_if_user_not_in_game(
            game_with_players_and_hands):
        with raises(UserNotInGameException):
            game_with_players_and_hands.play("computer3", 0)

    @staticmethod
    def test_play_game_over_should_raise(game_with_players_and_hands):
        game_with_players_and_hands.status = GameStatus.Encerrado
        with raises(GameOverException):
            game_with_players_and_hands.play(id_, 0)

    @staticmethod
    def test_play_not_player_turn_should_raise(game_with_players_and_hands):
        with raises(NotUserTurnException):
            game_with_players_and_hands.play("computer1", 0)

    @staticmethod
    def test_play_should_throw_card(game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)

        res = game_with_players_and_hands.play(id_, 0)
        assert res.maos[0]["cartas"][0]["rodada"] == 1

    @staticmethod
    def test_play_should_set_winner(game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)

        game_with_players_and_hands.play(id_, 0)
        res = game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)

        print(res.turno)
        game_with_players_and_hands.play(id_, 1)
        res = game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 1)

        assert res.vencedor == 1

    @staticmethod
    def test_won_should_add_points(game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)

        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)

        game_with_players_and_hands.play(id_, 1)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 1)

        assert game_with_players_and_hands.pontuacao == [0, 1]

    @staticmethod
    def test_won_should_add_partida(game_with_players_and_hands: Game):
        TestPlay.reset_partida(game_with_players_and_hands)

        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)

        game_with_players_and_hands.play(id_, 1)
        res = game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 1)

        assert len(game_with_players_and_hands.partidas) == 2

    @staticmethod
    def test_won_game_shouldnt_add_partida(game_with_players_and_hands: Game):
        TestPlay.reset_partida(game_with_players_and_hands)
        game_with_players_and_hands.partidas[0]["valor"] = 12

        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)

        game_with_players_and_hands.play(id_, 1)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 1)

        assert len(game_with_players_and_hands.partidas) == 1
        assert game_with_players_and_hands.status == GameStatus.Encerrado

    @staticmethod
    def test_won_with_3_should_add_points(game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)
        game_with_players_and_hands.partidas[-1]["valor"] = 3

        # round 1
        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)

        # round 2
        game_with_players_and_hands.play(id_, 1)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 2)  # winner

        assert game_with_players_and_hands.pontuacao == [0, 3]

    @staticmethod
    def test_result_should_only_contain_played_cards(
            game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)
        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)

        game_with_players_and_hands.play(id_, 1)
        res = game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 1)

        assert dict(res) == {
            'maos': [
                {'cartas': [{'naipe': 2, 'rodada': 1, 'valor': 7},
                            {'naipe': 0, 'rodada': 2, 'valor': 2}],
                 'jogador': 'ee81aa59cf1b41ea979e51f5170a128b'},
                {'cartas': [{'naipe': 2, 'rodada': 1, 'valor': 4},
                            {'naipe': 0, 'rodada': 2, 'valor': 4},
                            {'naipe': 1, 'rodada': None, 'valor': 7}],
                 'jogador': '23f2f1750af74f4b8d38683e4ed1b80b'},

                {'cartas': [{'naipe': 1, 'rodada': 1, 'valor': 7},
                            {'naipe': 1, 'rodada': 2, 'valor': 1}],
                 'jogador': 'computer1'},
                {'cartas': [{'naipe': 3, 'rodada': 1, 'valor': 7},
                            {'naipe': 3, 'rodada': 2, 'valor': 6}],
                 'jogador': 'computer2'}],
            'may_raise': [True, True],
            'turno': 3,
            'valor': 1,
            'vencedor': 1

        }

    @staticmethod
    def reset_partida(game_with_players_and_hands):
        for i in range(4):
            for j in range(3):
                game_with_players_and_hands.partidas[0]["maos"] \
                    [i]["cartas"][j]["rodada"] = None

    @staticmethod
    def test_play_without_partida_should_return_none(game_with_players):
        assert game_with_players.play(id_, 0) is None

    @staticmethod
    def test_play_with_mixed_order(game_with_players_and_hands):
        game_with_players_and_hands.partidas = []
        player_id_ = TOKEN_INFO.get("sub")
        game_with_players_and_hands.times = [
            [player_id_, "computer2"], [id_, "computer1"]
        ]
        game_with_players_and_hands.create_partida(player_id_)

        before_play = deepcopy(game_with_players_and_hands.get_current_partida(
            player_id_
        ))
        before_play.maos[0]["cartas"][0]["rodada"] = 1
        before_play.turno = 1
        res = game_with_players_and_hands.play(player_id_, 0)
        assert len(res.maos) == 1
        assert before_play == res

    @staticmethod
    def test_play_card_1_in_vieira_game(game_vieira, dao_mock):
        dao_mock.get.return_value = game_vieira
        res = partida_api.play.__wrapped__(game_vieira.id_,
                                           {"id_": 1},
                                           TOKEN_INFO,
                                           dao_mock)

        assert res[0] == 200
        assert game_vieira.partidas[0]["vencedor"] == 1

    @staticmethod
    def test_winner_partida_2(partida_vieira2):
        assert partida_vieira2.get_round_winner(1) == 1
        assert partida_vieira2.get_round_winner(2) == 0
        assert partida_vieira2.get_round_winner(3) == 2

    @staticmethod
    def test_winner_failed(dao_mock):
        game = Game()
        game.join(TOKEN_INFO.get("sub"))

        game.join("computer1")
        game.join("computer2")
        game.join("computer3")
        game.times = [[TOKEN_INFO.get("sub"), "computer1"],
                      ["computer2", "computer3"]]
        maos = [
            {
                "cartas": [
                    {
                        "naipe": 0,
                        "rodada": 1,
                        "valor": 3
                    },
                    {
                        "naipe": 0,
                        "rodada": 2,
                        "valor": 6
                    },
                    {
                        "naipe": 2,
                        "rodada": None,
                        "valor": 2
                    }
                ],
                "jogador": "nqG6zj27jyOAJdtj6ZJuByMbWa63"
            },
            {
                "cartas": [
                    {
                        "naipe": 0,
                        "rodada": 1,
                        "valor": 7
                    },
                    {
                        "naipe": 1,
                        "rodada": 2,
                        "valor": 7
                    },
                    {
                        "naipe": 3,
                        "rodada": None,
                        "valor": 3
                    }
                ],
                "jogador": "computer2"
            },
            {
                "cartas": [
                    {
                        "naipe": 1,
                        "rodada": 1,
                        "valor": 5
                    },
                    {
                        "naipe": 2,
                        "rodada": 2,
                        "valor": 4
                    },
                    {
                        "naipe": 0,
                        "rodada": None,
                        "valor": 4
                    }
                ],
                "jogador": "computer1"
            },
            {
                "cartas": [
                    {
                        "naipe": 3,
                        "rodada": 1,
                        "valor": 7
                    },
                    {
                        "naipe": 0,
                        "rodada": 2,
                        "valor": 2
                    },
                    {
                        "naipe": 3,
                        "rodada": 3,
                        "valor": 6
                    }
                ],
                "jogador": "computer3"
            }
        ]
        partida = Partida(maos=maos, turno=0)
        game.partidas = [dict(partida)]

        dao_mock.get.return_value = game
        res = partida_api.play.__wrapped__(game.id_,
                                           {"id_": 2},
                                           TOKEN_INFO,
                                           dao_mock)

        assert game.partidas[0]["vencedor"] is not None
        assert len(game.partidas) == 2
