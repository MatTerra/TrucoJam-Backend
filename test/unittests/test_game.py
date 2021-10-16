from nova_api.dao import is_valid_uuidv4

from utils.entity.game import Game, GameStatus


class TestGame:
    @staticmethod
    def test_init_empty_game():
        game = Game()
        assert is_valid_uuidv4(game.id_)
        assert game.senha == ""
        assert game.times == [[], []]
        assert game.partidas == []
        assert game.jogadores == []
        assert game.status == GameStatus.AguardandoJogadores

    @staticmethod
    def test_join_game_should_include_jogador():
        game = Game()
        user_id_ = "81dafcc184fe45daabfdb9c1331032f8"
        game.join(user_id_)
        assert user_id_ in game.jogadores
