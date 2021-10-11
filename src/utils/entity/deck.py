from random import shuffle

from dataclasses import dataclass, field
from typing import List

from utils.entity.Naipe import Suit
from utils.entity.card import Card, Value


def init_deck():
    cards = []
    for value in range(Value.QUEEN.value, Value.MANILHA.value + 1):
        for suit in range(Suit.Paus.value + 1):
            cards.append(Card(valor=value, naipe=Suit(suit)))
    cards.remove(Card(Suit.Espadas, Value.ACE.value))
    return cards


@dataclass
class Deck:
    cards: List[Card] = field(default_factory=init_deck)

    def shuffle(self):
        shuffle(self.cards)
