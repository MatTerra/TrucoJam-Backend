"""
Card model and values
"""
from dataclasses import dataclass, field
from enum import Enum
from functools import total_ordering


@total_ordering
class Value(Enum):
    """
    Enumeration of possible card values
    """
    QUEEN = 1
    KING = 2
    JACK = 3
    ACE = 4
    TWO = 5
    THREE = 6
    MANILHA = 7

    def __gt__(self, other):
        # pylint: disable=W0143
        return self.value > other.value

    def __eq__(self, other):
        # pylint: disable=W0143
        return self.value == other.value


@total_ordering
class Suit(Enum):
    """
    Enumeration of possible card suits
    """
    OUROS = 0
    ESPADAS = 1
    COPAS = 2
    PAUS = 3

    def __gt__(self, other):
        # pylint: disable=W0143
        return self.value > other.value

    def __eq__(self, other):
        # pylint: disable=W0143
        return self.value == other.value


@total_ordering
@dataclass
class Card:
    """
    Card model
    """
    naipe: Suit = field(default=None, compare=True)
    valor: Value = field(default=None, compare=True)

    def __lt__(self, other):
        return self.valor < other.valor or \
               (self.valor == other.valor
                and self.valor == Value.MANILHA
                and self.naipe < other.naipe)

    def __gt__(self, other):
        return self.valor > other.valor or \
               (self.valor == other.valor
                and self.valor == Value.MANILHA
                and self.naipe > other.naipe)
