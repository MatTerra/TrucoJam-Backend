from dataclasses import dataclass, field
from enum import Enum
from functools import total_ordering

from utils.entity.Naipe import Suit


class Value(Enum):
    QUEEN = 1
    KING = 2
    JACK = 3
    ACE = 4
    TWO = 5
    THREE = 6
    MANILHA = 7


@total_ordering
@dataclass
class Card:
    naipe: Suit = field(default=None, compare=True)
    valor: int = field(default=None, compare=True)

    def __lt__(self, other):
        return self.valor < other.valor or \
               (self.valor == other.valor and self.valor == Value.MANILHA.value
                and self.naipe.value < other.naipe.value)

    def __gt__(self, other):
        return self.valor > other.valor or \
               (self.valor == other.valor and self.valor == Value.MANILHA.value
                and self.naipe.value > other.naipe.value)
