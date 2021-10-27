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

    @staticmethod
    def test_may_use_max():
        cards = [Card(naipe=Suit.COPAS, valor=Value.MANILHA),
                 Card(naipe=Suit.PAUS, valor=Value.MANILHA),
                 Card(naipe=Suit.COPAS, valor=Value.ACE),
                 Card(naipe=Suit.PAUS, valor=Value.ACE)]

        assert max(cards) == Card(naipe=Suit.PAUS, valor=Value.MANILHA)

        cards = [Card(naipe=Suit.COPAS, valor=Value.THREE),
                 Card(naipe=Suit.PAUS, valor=Value.THREE),
                 Card(naipe=Suit.COPAS, valor=Value.ACE),
                 Card(naipe=Suit.PAUS, valor=Value.KING)]
        valores_cartas = list(map(lambda card: card.valor, cards))
        if max(valores_cartas) != Value.MANILHA \
                and valores_cartas.count(max(valores_cartas)) > 1:
            assert True
        else:
            assert False
