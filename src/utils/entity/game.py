"""
Game model module
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from nova_api.entity import Entity

from utils.exceptions.full_game_exception import FullGameException
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

    def join(self, user_id_, senha: str = ""):
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
