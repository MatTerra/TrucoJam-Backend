from dataclasses import dataclass, field
from enum import Enum

from nova_api.entity import Entity


def pontuacao_vazia():
    return [0, 0]


def times_vazios():
    return [[], []]


class GameStatus(Enum):
    AguardandoJogadores = 0
    Jogando = 1
    Encerrado = 2


@dataclass
class Game(Entity):
    pontuacao: list = field(default_factory=pontuacao_vazia)
    senha: str = ""
    times: list = field(default_factory=times_vazios)
    partidas: list = field(default_factory=list)
    status: GameStatus = GameStatus.AguardandoJogadores
