from utils.entity.card import Card, Value, Suit
from utils.entity.deck import Deck

cards = [
    Card(naipe=Suit.OUROS, valor=Value.QUEEN),
    Card(naipe=Suit.ESPADAS, valor=Value.QUEEN),
    Card(naipe=Suit.COPAS, valor=Value.QUEEN),
    Card(naipe=Suit.PAUS, valor=Value.QUEEN),
    Card(naipe=Suit.OUROS, valor=Value.KING),
    Card(naipe=Suit.ESPADAS, valor=Value.KING),
    Card(naipe=Suit.COPAS, valor=Value.KING),
    Card(naipe=Suit.PAUS, valor=Value.KING),
    Card(naipe=Suit.OUROS, valor=Value.JACK),
    Card(naipe=Suit.ESPADAS, valor=Value.JACK),
    Card(naipe=Suit.COPAS, valor=Value.JACK),
    Card(naipe=Suit.PAUS, valor=Value.JACK),
    Card(naipe=Suit.OUROS, valor=Value.ACE),
    Card(naipe=Suit.COPAS, valor=Value.ACE),
    Card(naipe=Suit.PAUS, valor=Value.ACE),
    Card(naipe=Suit.OUROS, valor=Value.TWO),
    Card(naipe=Suit.ESPADAS, valor=Value.TWO),
    Card(naipe=Suit.COPAS, valor=Value.TWO),
    Card(naipe=Suit.PAUS, valor=Value.TWO),
    Card(naipe=Suit.OUROS, valor=Value.THREE),
    Card(naipe=Suit.ESPADAS, valor=Value.THREE),
    Card(naipe=Suit.COPAS, valor=Value.THREE),
    Card(naipe=Suit.PAUS, valor=Value.THREE),
    Card(naipe=Suit.OUROS, valor=Value.MANILHA),
    Card(naipe=Suit.ESPADAS, valor=Value.MANILHA),
    Card(naipe=Suit.COPAS, valor=Value.MANILHA),
    Card(naipe=Suit.PAUS, valor=Value.MANILHA)
]


class TestDeck:

    @staticmethod
    def test_new_deck_should_contain_all_cards():
        d = Deck()

        assert d.cards == cards

    @staticmethod
    def test_new_deck_should_not_contain_A_of_spades_as_A():
        d = Deck()

        c = Card(Suit.ESPADAS, Value.ACE)

        assert c not in d.cards

    @staticmethod
    def test_shuffle_deck_should_change_order():
        d = Deck()

        d.shuffle()

        assert d.cards != cards
