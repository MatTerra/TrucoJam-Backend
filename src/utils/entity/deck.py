"""
Deck model module
"""
from random import shuffle

from dataclasses import dataclass, field
from typing import List

from utils.entity.card import Card, Value, Suit


def init_deck() -> List[Card]:
    """
    Deck generation function
    :return: Full deck
    """
    cards = []
    for value in range(Value.QUEEN.value, Value.MANILHA.value + 1):
        for suit in range(Suit.PAUS.value + 1):
            cards.append(Card(valor=Value(value), naipe=Suit(suit)))
    cards.remove(Card(Suit.ESPADAS, Value.ACE))
    return cards


@dataclass
class Deck:
    """
    Deck of cards model
    """
    cards: List[Card] = field(default_factory=init_deck)

    def shuffle(self) -> None:
        """
        This method shuffles the deck of cards at random.
        """
        shuffle(self.cards)

    def buy_card(self) -> Card:
        return self.cards.pop(0)
