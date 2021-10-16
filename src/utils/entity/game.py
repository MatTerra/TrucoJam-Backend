"""
Game model module
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from nova_api.entity import Entity


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
        self.jogadores.append(user_id_)
