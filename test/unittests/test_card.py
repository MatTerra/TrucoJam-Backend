from utils.entity.Naipe import Suit
from utils.entity.card import Card, Value


class TestCard:
    @staticmethod
    def test_may_compare_two_cards_with_different_values():
        assert Card(naipe=Suit.Espadas, valor=Value.QUEEN.value) \
               < Card(naipe=Suit.Espadas, valor=Value.KING.value)

    @staticmethod
    def test_may_compare_two_MANILHA():
        assert Card(naipe=Suit.Copas, valor=Value.MANILHA.value) \
               < Card(naipe=Suit.Paus, valor=Value.MANILHA.value)

    @staticmethod
    def test_may_compare_two_card_with_same_value():
        assert not Card(naipe=Suit.Copas, valor=Value.ACE.value) \
                   < Card(naipe=Suit.Paus, valor=Value.ACE.value) \
               and not Card(naipe=Suit.Copas, valor=Value.ACE.value) \
                   > Card(naipe=Suit.Paus, valor=Value.ACE.value)
