from nova_api.dao import is_valid_uuidv4
from pytest import raises, mark

from utils.entity.game import Game, GameStatus
from utils.exceptions.user_already_in_game_exception import \
    UserAlreadyInGameException
from utils.exceptions.wrong_password_exception import WrongPasswordException

user_id_ = "81dafcc184fe45daabfdb9c1331032f8"


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
        game.join(user_id_)
        assert user_id_ in game.jogadores

    @staticmethod
    def test_join_game_wrong_password_should_raise_exception():
        game = Game(senha="123")
        with raises(WrongPasswordException):
            game.join(user_id_, "wrong")

    @staticmethod
    @mark.parametrize("senha",[
        "1123",
        "abc",
        "",
        None
    ])
    def test_join_game_with_no_password_should_allow_any_password(senha):
        game = Game()
        game.join(user_id_, senha)
        assert user_id_ in game.jogadores

    @staticmethod
    def test_join_game_with_player_already_registered_should_raise():
        game = Game()
        game.join(user_id_)

        with raises(UserAlreadyInGameException):
            game.join(user_id_)

