from pytest import raises

from test.unittests import *
from utils.entity.game import GameStatus
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
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)
        game_with_players_and_hands.play("computer1", 0)
        game_with_players_and_hands.play("computer2", 1)

        game_with_players_and_hands.play("computer2", 0)
        game_with_players_and_hands.play(id_, 1)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 1)
        res = game_with_players_and_hands.play("computer1", 1)

        assert res.vencedor == 1

    @staticmethod
    def test_won_should_add_points(game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)

        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)
        game_with_players_and_hands.play("computer1", 0)
        game_with_players_and_hands.play("computer2", 1)

        game_with_players_and_hands.play("computer2", 0)
        game_with_players_and_hands.play(id_, 1)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 1)
        game_with_players_and_hands.play("computer1", 1)

        assert game_with_players_and_hands.pontuacao == [0, 1]

    @staticmethod
    def test_won_with_3_should_add_points(game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)
        game_with_players_and_hands.partidas[-1]["valor"] = 3

        # round 1
        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)
        game_with_players_and_hands.play("computer1", 1)
        game_with_players_and_hands.play("computer2", 1)

        # round 2
        game_with_players_and_hands.play("computer2", 2)
        game_with_players_and_hands.play(id_, 1)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 2) # winner
        game_with_players_and_hands.play("computer1", 0)

        assert game_with_players_and_hands.pontuacao == [0, 3]

    @staticmethod
    def test_result_should_only_contain_played_cards(
            game_with_players_and_hands):
        TestPlay.reset_partida(game_with_players_and_hands)
        game_with_players_and_hands.play(id_, 0)
        game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)
        game_with_players_and_hands.play("computer1", 0)
        game_with_players_and_hands.play("computer2", 1)

        game_with_players_and_hands.play("computer2", 0)
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
                {'cartas': [{'naipe': 1, 'rodada': 1, 'valor': 7}],
                 'jogador': 'computer1'},
                {'cartas': [{'naipe': 3, 'rodada': 2, 'valor': 6},
                            {'naipe': 3, 'rodada': 1, 'valor': 7}],
                 'jogador': 'computer2'}],
            'may_raise': True,
            'turno': 2,
            'valor': 1,
            'vencedor': None
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
