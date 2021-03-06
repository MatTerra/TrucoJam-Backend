from test.unittests import *


class TestBots:
    @staticmethod
    def test_computer_should_auto_play_if_turn(game_with_players_and_hands):
        game_with_players_and_hands.play(id_, 0)
        res = game_with_players_and_hands.play(TOKEN_INFO.get("sub"), 0)
        assert res.turno == 0
        assert len(res.maos) == 4
        print(res)
        assert len(res.maos[3]["cartas"]) == 2
        assert len(res.maos[1]["cartas"]) == 3
        assert len(res.maos[0]["cartas"]) == 1
        assert len(res.maos[2]["cartas"]) == 1

    @staticmethod
    def test_start_on_ready_with_teams_on_players_should_start(
            game_with_players
    ):
        game_with_players.times = [[id_], [TOKEN_INFO.get("sub")]]
        game_with_players.create_partida(id_)
        assert game_with_players.times == [
            [id_, "computer1"],
            [TOKEN_INFO.get("sub"), "computer2"]
        ]
