"""
Game model module
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from nova_api.entity import Entity

from utils.exceptions.full_game_exception import FullGameException
from utils.exceptions.invalid_team_exception import InvalidTeamException
from utils.exceptions.not_waiting_for_players_exception import \
    NotWaitingForPlayersException
from utils.exceptions.user_already_in_game_exception import \
    UserAlreadyInGameException
from utils.exceptions.wrong_password_exception import WrongPasswordException


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

    def join(self, user_id_, senha: str = "") -> None:
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

        if user_id_ in self.jogadores:
            raise UserAlreadyInGameException(f"User {user_id_} "
                                             f"already in game.")

        if self.senha and senha != self.senha:
            raise WrongPasswordException(f"Incorrect password: {senha} "
                                         f"for game {self.id_}.")

        self.jogadores.append(user_id_)

        if len(self.jogadores) == 4:
            self.status = GameStatus.Jogando
    
    def join_team(self, user_id_,team_id_):
        if team_id_ not in range (0,1):
            raise InvalidTeamException(f"team index {team_id_} "
                                       f"out of range")
        
        self.times[team_id_].append(user_id_)
        
