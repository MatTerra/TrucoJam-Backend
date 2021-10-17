from dataclasses import dataclass, field, fields
from typing import List


@dataclass
class Partida:
    turno: int = field(default=0)
    valor: int = field(default=1)
    vencedor: int = field(default=None)
    maos: List[dict] = field(default_factory=list)
    may_raise: bool = field(default=True)

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value