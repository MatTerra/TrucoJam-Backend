"""
Game model module
"""
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from functools import reduce

from nova_api.entity import Entity

from utils.entity.deck import Deck
from utils.entity.partida import Partida
from utils.exceptions.full_game_exception import FullGameException
from utils.exceptions.full_team_exception import FullTeamException
from utils.exceptions.game_already_started_exception import \
    GameAlreadyStartedException
from utils.exceptions.game_not_ready_exception import GameNotReadyException
from utils.exceptions.invalid_team_exception import InvalidTeamException
from utils.exceptions.game_over_exception import GameOverException
from utils.exceptions.not_waiting_for_players_exception import \
    NotWaitingForPlayersException
from utils.exceptions.partida_ongoing_exception import PartidaOngoingException
from utils.exceptions.user_already_in_game_exception import \
    UserAlreadyInGameException
from utils.exceptions.user_already_in_team_exception import \
    UserAlreadyInTeamException
from utils.exceptions.user_not_in_game_exception import UserNotInGameException
from utils.exceptions.wrong_password_exception import WrongPasswordException

ROUNDS_TO_WIN_PARTIDA = 2
TIMES = 2
ROUNDS_IN_PARTIDA = 3


def pontuacao_vazia() -> List[int]:
    """
    Simple empty pontuacao generator

    :return: Empty pontuacao list
    """
    return [0, 0]


def times_vazios() -> List[List[str]]:
    """
    Simple empty times generator

    :return: Empty times list
    """
    return [[], []]


class GameStatus(Enum):
    """
    Game status enumeration
    """
    AguardandoJogadores = 0
    Pronto = 1
    Jogando = 2
    Encerrado = 3


@dataclass
class Game(Entity):
    """
    Game model
    """
    pontuacao: list = field(default_factory=pontuacao_vazia)
    senha: str = ""
    times: list = field(default_factory=times_vazios)
    partidas: list = field(default_factory=list)
    jogadores: list = field(default_factory=list)
    status: GameStatus = GameStatus.AguardandoJogadores

    def play(self, user_id_: str, card_id_: int) -> Optional[Partida]:
        """
        Plays the card with card_id_ for the user if it is its turn.

        :raise UserNotInGameException: If user is not in game
        :raise GameOverException: If game status is Encerrado
        :raise NotUserTurnException: If it isn't the user's turn
        :raise PartidaOverException: If the current partida is already won
        :raise CardAlreadyPlayedException: If card_id_ has been played before


        :param user_id_: The ID of the user that is playing
        :param card_id_: The ID of the card to play
        :return: The updated partida
        """
        if not self.is_user_a_participant(user_id_):
            raise UserNotInGameException(f"User {user_id_} not found in "
                                         f"game {self.id_}.")

        if self.status == GameStatus.Encerrado:
            raise GameOverException(f"Game {self.id_} is already over.")

        if len(self.partidas) == 0:
            return None

        partida = self.__get_last_partida()

        user_index = self.__get_user_index(user_id_)
        partida.play(user_index, card_id_)

        vencedor = None
        while self.__is_computer_next(partida) and not vencedor:
            if partida.get_current_round() > 3:
                break
            partida.play(partida.turno, partida.get_current_round() - 1)
            vencedor = self.__check_partida_winner(partida)
            if vencedor:
                break

        self.partidas[-1] = dict(partida)

        if vencedor \
                and self.pontuacao[0] < 12 \
                and self.pontuacao[1] < 12:
            self.__create_partida()

        if self.pontuacao[0] >= 12 \
                or self.pontuacao[1] >= 12:
            self.status = GameStatus.Encerrado

        partida_to_return = deepcopy(partida)
        Game.__filter_hands(partida_to_return, user_id_)

        return partida_to_return

    def __is_computer_next(self, partida):
        return self.__get_players_in_playing_order()[
            partida.turno].startswith("computer")

    def __create_partida(self):
        self.partidas.append(dict(
            Partida(maos=self.__generate_player_hands())
        ))

    def is_user_a_participant(self, user_id_: str) -> bool:
        """
        Checks that the user is part of the game

        :param user_id_: The ID of the user to check
        :return: True if user is in game, False otherwise
        """
        return user_id_ in self.jogadores

    def __get_last_partida(self) -> Optional[Partida]:
        """
        Returns the last partida in the partidas list as a Partida object
        :return: The partida
        """
        if len(self.partidas) > 0:
            return Partida(**self.partidas[-1])
        return None

    def __get_user_index(self, user_id_):
        return self.__get_players_in_playing_order().index(user_id_)

    def __get_players_in_playing_order(self):
        return sum(zip(*self.times), ())

    def __check_partida_winner(self, partida: Partida) -> Optional[int]:
        """
        Checks if the partida has been won by any team. If it has, registers it
        and sums the points
        :param partida: Partida to check
        :return: The winning team index or None
        """
        winners = [self.jogadores[partida.get_round_winner(round_)]
                   for round_ in range(1, ROUNDS_IN_PARTIDA + 1)
                   if partida.get_round_winner(round_)]

        win_team = [self.__get_user_team(user) for user in winners]
        print(f"{winners}")
        for team in range(TIMES):
            if win_team.count(team) == ROUNDS_TO_WIN_PARTIDA:
                partida.vencedor = team

        if partida.vencedor is not None:
            self.pontuacao[partida.vencedor] += partida.valor

        return partida.vencedor

    def __get_user_team(self, user_id_: str) -> Optional[int]:
        """
        Checks the team to verify in which team the player is.
        :param user_id_: The ID of the player to check
        :return: The team the player is in
        """
        for i in range(2):
            if user_id_ in self.times[i]:
                return i

        return None

    def join(self, user_id_: str, senha: str = "") -> None:
        """
        Join game and updates the status if game full after join.

        :raise FullGameException: If the game already has 4 players.
        :raise NotWaitingForPlayersException: If the game is not in the \
        waiting state.
        :raise UserAlreadyInGameException: If user is already participating \
        in this game.
        :raise WrongPasswordException: If the senha informed doesn't match \
        the game senha.

        :param user_id_: User joining the game.
        :param senha: Senha of the game.
        """
        if len(self.jogadores) == 4:
            raise FullGameException(f"Game {self.id_} is already full.")

        if self.status != GameStatus.AguardandoJogadores:
            raise NotWaitingForPlayersException(f"Game {self.id_} not "
                                                f"waiting for players.")

        if self.is_user_a_participant(user_id_):
            raise UserAlreadyInGameException(f"User {user_id_} "
                                             f"already in game.")

        if self.senha and senha != self.senha:
            raise WrongPasswordException(f"Incorrect password: {senha} "
                                         f"for game {self.id_}.")

        self.jogadores.append(user_id_)

        if len(self.jogadores) == 4:
            self.status = GameStatus.Pronto

    def join_team(self, user_id_, team_id_):
        if self.status == GameStatus.Encerrado:
            raise GameOverException(f"User {user_id_} tried to "
                                    f"change team in a game that already "
                                    f"ended.")

        if not self.is_user_a_participant(user_id_):
            raise UserNotInGameException(f"User {user_id_} not found in "
                                         f"game {self.id_}.")

        team = self.__get_user_team(user_id_)

        if self.__get_last_partida():
            raise GameAlreadyStartedException(f"User {user_id_} tried to "
                                              f"change team after game start.")

        if team == team_id_:
            raise UserAlreadyInTeamException(f"User {user_id_} tried to join "
                                             f"the {team_id_} team twice")

        if team_id_ not in [0, 1]:
            raise InvalidTeamException(f"Team index {team_id_} "
                                       f"out of range.")

        if len(self.times[team_id_]) == 2:
            raise FullTeamException(f"Team {team_id_} is already full")

        if team is not None:
            self.times[team].remove(user_id_)

        self.__join_team(user_id_, team_id_)

    def join_team_bot(self, user_id_: str, team_id_: int):
        if not self.is_user_a_participant(user_id_):
            raise UserNotInGameException("User tried to join a bot in a "
                                         "game he is not in")

        if self.status == GameStatus.Encerrado:
            raise GameOverException("Tried to add a bot in an ended "
                                    "game")

        if self.__get_last_partida():
            raise GameAlreadyStartedException(f"User tried to add "
                                              f"bot to team after game start.")

        if team_id_ not in [0, 1]:
            raise InvalidTeamException(f"Team index {team_id_} "
                                       f"out of range.")

        if len(self.times[team_id_]) == 2:
            raise FullTeamException(f"Team {team_id_} is already full")

        if len(self.jogadores) == 4:
            raise FullGameException("User tried to add a bot in a full game")

        computer_number = len(
            [player for player in self.__get_computer_players()]
        ) + 1
        computer_name = 'computer' + str(computer_number)

        self.jogadores.append(computer_name)
        self.__join_team(computer_name, team_id_)

        if len(self.jogadores) == 4:
            self.status = GameStatus.Pronto

    def remove_team_bot(self, user_id_: str, team_id_: int):
        if user_id_ not in self.jogadores:
            raise UserNotInGameException("User tried to join a bot in a "
                                         "game he is not in")

        if self.status == GameStatus.Encerrado:
            raise GameOverException("Tried to create a partida in an ended "
                                    "game")

        if self.__get_last_partida():
            raise GameAlreadyStartedException(f"User tried to remove "
                                              f"bot to team after game start.")

        if team_id_ not in [0, 1]:
            raise InvalidTeamException(f"Team index {team_id_} "
                                       f"out of range.")

        if len([player for player in self.times[team_id_]
                if player.startswith("computer")]) == 0:
            raise UserNotInGameException("User tried to remove computer from "
                                         "a team without computers")

        self.__reorganize_computers(team_id_)

        if self.status == GameStatus.Pronto:
            self.status = GameStatus.AguardandoJogadores

    def __reorganize_computers(self, team_id_):
        old_teams = [deepcopy(self.times[0]), deepcopy(self.times[1])]
        self.times = [
            [player for player in time
             if not player.startswith("computer")]
            for time in self.times
        ]
        computers = self.__get_computer_players()[:-1]
        self.jogadores = [player for player in self.jogadores
                          if not player.startswith("computer")]
        self.jogadores.extend(computers)
        for computer in computers:
            for time in range(TIMES):
                if self.team_should_have_a_bot(time, old_teams, team_id_):
                    self.__join_team(computer, time)
                    continue

    def team_should_have_a_bot(self, team, old_teams, team_id_to_remove):
        return (len(self.times[team]) < len(old_teams[team])
                and team_id_to_remove != team) \
               or (team_id_to_remove == team
                   and len(self.times[team]) + 1 < len(old_teams[team]))

    def __join_team(self, user_id_, team_id_):
        self.times[team_id_].append(user_id_)

    def create_partida(self, user_id_):
        if self.status == GameStatus.Encerrado:
            raise GameOverException("Tried to create a partida in an ended "
                                    "game")

        if not self.is_user_a_participant(user_id_):
            raise UserNotInGameException(f"User {user_id_} not found in "
                                         f"game {self.id_}.")

        if self.__get_last_partida():
            raise PartidaOngoingException("Tried to create a partida in a "
                                          "game with a partida in progress")

        if self.status == GameStatus.AguardandoJogadores:
            raise GameNotReadyException("Still waiting for players")

        if self.status == GameStatus.Pronto:
            if self.__all_human_players_are_in_teams():
                self.__distribute_computers_on_teams()
            else:
                raise GameNotReadyException("Not all players chose a team")

        self.status = GameStatus.Jogando
        self.__create_partida()

    def __all_human_players_are_in_teams(self):
        human_players = 4 - len(self.__get_computer_players())
        players_in_teams = len(self.__get_players_in_playing_order())
        return human_players <= players_in_teams

    def __distribute_computers_on_teams(self):
        for computer_player in self.__get_computer_players():
            if computer_player in self.__get_players_in_playing_order():
                continue
            for time in range(TIMES):
                if self.__team_is_not_full(time):
                    self.__join_team(computer_player, time)
                    break

    def __get_computer_players(self):
        return [player for player in self.jogadores
                if player.startswith("computer")]

    def __team_is_not_full(self, time):
        return len(self.times[time]) < 2

    def __create_partida(self):
        self.partidas.append(dict(
            Partida(maos=self.__generate_player_hands())
        ))

    def __generate_player_hands(self):
        deck = Deck()
        deck.shuffle()
        maos = [
            {
                "jogador": jogador,
                "cartas": [
                    {"naipe": carta.naipe.value,
                     "valor": carta.valor.value,
                     "rodada": None}
                    for carta in [deck.buy_card(),
                                  deck.buy_card(),
                                  deck.buy_card()]]}
            for jogador in self.__get_players_in_playing_order()]
        return maos

    def get_player_hand(self, user_id_):
        return [mao for mao in self.__get_last_partida().maos
                if mao.get("jogador") == user_id_][0]

    def get_current_partida(self, user_id_: str) -> Optional[Partida]:
        """
        Returns the current partida correctly formatted for the player, that
        is, excludes other players cards.

        :raise UserNotInGameException: If user is not a player in this game.
        :raise GameOverException: If game status is Encerrado

        :param user_id_: The player user_id_ to get the partida for.
        :return: The partida viewed by the player.
        """
        if not self.is_user_a_participant(user_id_):
            raise UserNotInGameException(f"User {user_id_} not found in "
                                         f"game {self.id_}.")

        if self.status == GameStatus.Encerrado:
            raise GameOverException(f"Game {self.id_} is already over.")

        if len(self.partidas) == 0:
            return None

        partida = deepcopy(self.__get_last_partida())

        if partida:
            Game.__filter_hands(partida, user_id_)

        return partida

    @staticmethod
    def __filter_hands(partida, user_id_):
        partida.maos = [mao for mao in partida.maos
                        if mao.get("jogador") == user_id_
                        or Game.__hand_has_played_cards(mao)]
        Game.__filter_played_cards(partida.maos, user_id_)

    @staticmethod
    def __filter_played_cards(maos, user_id_):
        for mao in maos:
            if mao.get("jogador") == user_id_:
                continue
            mao["cartas"] = [carta for carta in mao.get("cartas")
                             if carta.get("rodada") is not None]

    @staticmethod
    def __hand_has_played_cards(mao):
        for carta in mao.get("cartas"):
            if carta.get("rodada") is not None:
                return True
        return False

    def game_to_return(self):
        dict_to_return = dict(self)
        dict_to_return.pop("senha")
        if len(dict_to_return["partidas"]) >= 1:
            dict_to_return["partidas"] = dict_to_return["partidas"][:-1]
        return dict_to_return

    def raise_game(self, user_id_):
        if not self.is_user_a_participant(user_id_):
            raise UserNotInGameException(f"User {user_id_} not found in "
                                         f"game {self.id_}.")

        if self.status == GameStatus.Encerrado:
            raise GameOverException(f"Game {self.id_} is already over.")

        partida = self.__get_last_partida()

        if not partida:
            raise GameNotReadyException(f"User {user_id_} tried to raise on "
                                        f"a game before start")

        partida.raise_value(self.__get_user_index(user_id_),
                            self.__get_user_team(user_id_))

        self.partidas[-1] = dict(partida)

    def fold_game(self, user_id_):
        if not self.is_user_a_participant(user_id_):
            raise UserNotInGameException(f"User {user_id_} not found in "
                                         f"game {self.id_}.")

        if self.status == GameStatus.Encerrado:
            raise GameOverException(f"Game {self.id_} is already over.")

        partida = self.__get_last_partida()

        if not partida:
            raise GameNotReadyException(f"User {user_id_} tried to raise on "
                                        f"a game before start")

        partida.fold(self.__get_user_team(user_id_))

        self.partidas[-1] = dict(partida)
