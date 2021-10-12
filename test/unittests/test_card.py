from utils.entity.card import Card, Value, Suit


class TestCard:
    @staticmethod
    def test_may_compare_two_cards_with_different_values():
        assert Card(naipe=Suit.ESPADAS, valor=Value.QUEEN) \
               < Card(naipe=Suit.ESPADAS, valor=Value.KING)

    @staticmethod
    def test_may_compare_two_MANILHA():
        assert Card(naipe=Suit.COPAS, valor=Value.MANILHA) \
               < Card(naipe=Suit.PAUS, valor=Value.MANILHA)

    @staticmethod
    def test_may_compare_two_card_with_same_value():
        assert not Card(naipe=Suit.COPAS, valor=Value.ACE) \
                   < Card(naipe=Suit.PAUS, valor=Value.ACE) \
               and not Card(naipe=Suit.COPAS, valor=Value.ACE) \
                   > Card(naipe=Suit.PAUS, valor=Value.ACE)
