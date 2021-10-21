"""
Game model module
"""
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from nova_api.entity import Entity

from utils.entity.partida import Partida
from utils.exceptions.full_game_exception import FullGameException
from utils.exceptions.game_over_exception import GameOverException
from utils.exceptions.not_waiting_for_players_exception import \
    NotWaitingForPlayersException
from utils.exceptions.user_already_in_game_exception import \
    UserAlreadyInGameException
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
    Jogando = 1
    Encerrado = 2


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

        user_index = self.jogadores.index(user_id_)
        partida.play(user_index, card_id_)

        self.__check_partida_winner(partida)

        self.partidas[-1] = dict(partida)

        partida_to_return = deepcopy(partida)
        Game.__filter_hands(partida_to_return, user_id_)

        return partida_to_return

    def is_user_a_participant(self, user_id_: str) -> bool:
        """
        Checks that the user is part of the game

        :param user_id_: The ID of the user to check
        :return: True if user is in game, False otherwise
        """
        return user_id_ in self.jogadores

    def __get_last_partida(self) -> Partida:
        """
        Returns the last partida in the partidas list as a Partida object
        :return: The partida
        """
        return Partida(**self.partidas[-1])

    def __check_partida_winner(self, partida: Partida) -> None:
        """
        Checks if the partida has been won by any team. If it has, registers it
        and sums the points
        :param partida: Partida to check
        :return:
        """
        winners = [partida.get_round_winner(round_)
                   for round_ in range(ROUNDS_IN_PARTIDA)
                   if partida.get_round_winner(round_)]

        win_team = [self.__get_user_team(user) for user in winners]

        for team in range(TIMES):
            if win_team.count(team) == ROUNDS_TO_WIN_PARTIDA:
                partida.vencedor = team

        if partida.vencedor is not None:
            self.pontuacao[partida.vencedor] += partida.valor

    def __get_user_team(self, user: int) -> int:
        """
        Checks the team to verify in which team the player is.
        :param user: The index of the player in the jogadores list
        :return: The team the player is in
        """
        for i in range(2):
            if user in self.times[i]:
                return i

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
            self.status = GameStatus.Jogando

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

        partida = self.__get_last_partida()
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
