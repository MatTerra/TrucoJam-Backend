from utils.entity.Naipe import Suit
from utils.entity.card import Card, Value
from utils.entity.deck import Deck

cards = [
    Card(naipe=Suit.Ouros, valor=Value.QUEEN.value),
    Card(naipe=Suit.Espadas, valor=Value.QUEEN.value),
    Card(naipe=Suit.Copas, valor=Value.QUEEN.value),
    Card(naipe=Suit.Paus, valor=Value.QUEEN.value),
    Card(naipe=Suit.Ouros, valor=Value.KING.value),
    Card(naipe=Suit.Espadas, valor=Value.KING.value),
    Card(naipe=Suit.Copas, valor=Value.KING.value),
    Card(naipe=Suit.Paus, valor=Value.KING.value),
    Card(naipe=Suit.Ouros, valor=Value.JACK.value),
    Card(naipe=Suit.Espadas, valor=Value.JACK.value),
    Card(naipe=Suit.Copas, valor=Value.JACK.value),
    Card(naipe=Suit.Paus, valor=Value.JACK.value),
    Card(naipe=Suit.Ouros, valor=Value.ACE.value),
    Card(naipe=Suit.Copas, valor=Value.ACE.value),
    Card(naipe=Suit.Paus, valor=Value.ACE.value),
    Card(naipe=Suit.Ouros, valor=Value.TWO.value),
    Card(naipe=Suit.Espadas, valor=Value.TWO.value),
    Card(naipe=Suit.Copas, valor=Value.TWO.value),
    Card(naipe=Suit.Paus, valor=Value.TWO.value),
    Card(naipe=Suit.Ouros, valor=Value.THREE.value),
    Card(naipe=Suit.Espadas, valor=Value.THREE.value),
    Card(naipe=Suit.Copas, valor=Value.THREE.value),
    Card(naipe=Suit.Paus, valor=Value.THREE.value),
    Card(naipe=Suit.Ouros, valor=Value.MANILHA.value),
    Card(naipe=Suit.Espadas, valor=Value.MANILHA.value),
    Card(naipe=Suit.Copas, valor=Value.MANILHA.value),
    Card(naipe=Suit.Paus, valor=Value.MANILHA.value)
]


class TestDeck:

    @staticmethod
    def test_new_deck_should_contain_all_cards():
        d = Deck()

        assert d.cards == cards

    @staticmethod
    def test_new_deck_should_not_contain_A_of_spades_as_A():
        d = Deck()

        c = Card(Suit.Espadas, Value.ACE.value)

        assert c not in d.cards

    @staticmethod
    def test_shuffle_deck_should_change_order():
        d = Deck()

        d.shuffle()

        assert d.cards != cards
