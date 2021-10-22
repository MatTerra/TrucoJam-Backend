from dataclasses import dataclass, field, fields
from typing import List

from utils.entity.card import Card, Suit, Value
from utils.exceptions.card_already_played_exception import \
    CardAlreadyPlayedException
from utils.exceptions.invalid_card_exception import InvalidCardException
from utils.exceptions.not_user_turn_exception import NotUserTurnException
from utils.exceptions.partida_over_exception import PartidaOverException


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

    def play(self, user_index: int, card_id_: int):
        if self.vencedor is not None:
            raise PartidaOverException("User tried to play card on ended "
                                       "partida.")

        if user_index != self.turno:
            raise NotUserTurnException("User tried to play out of turn")

        if card_id_ not in [0, 1, 2]:
            raise InvalidCardException(f"User tried to play invalid card "
                                       f"{card_id_}")

        if self.__is_user_card_played(user_index, card_id_):
            raise CardAlreadyPlayedException("User tried to replay a card")

        current_round = self.__get_current_round()

        self.maos[user_index]["cartas"][card_id_]["rodada"] = current_round

        self.turno = self.__get_next_turn(current_round)

    def __is_user_card_played(self, user_index, card_id_):
        return self.__get_user_card_round(user_index, card_id_) is not None

    def __get_user_card_round(self, user_index, card_id_):
        return self.__get_user_cards(user_index)[card_id_].get("rodada")

    def __get_user_cards(self, user_index):
        return self.maos[user_index]["cartas"]

    def __get_current_round(self):
        last_player = (self.turno - 1) % 4

        last_round_last_player = self.__get_user_last_round(last_player)
        player_last_round = self.__get_user_last_round(self.turno)

        if player_last_round == last_round_last_player:
            return player_last_round + 1

        return last_round_last_player

    def __get_user_last_round(self, user_id_):
        return max(
            [self.__get_user_card_round(user_id_, card)
             for card in range(3)
             if
             self.__get_user_card_round(user_id_, card)],
            default=0)

    def __get_next_turn(self, round):
        winner = self.get_round_winner(round)

        if winner:
            return winner

        return (self.turno + 1) % 4

    def get_round_winner(self, round):
        round_cards = self.__get_round_cards(round)

        if len(round_cards) == 4:
            return round_cards.index(max(round_cards))
        return None

    def __get_round_cards(self, round):
        maos_ = [[Card(Suit(carta.get("naipe")), Value(carta.get("valor"))) for
                  carta in mao.get("cartas") if carta.get("rodada") == round]
                 for mao in self.maos]

        while [] in maos_:
            maos_.remove([])

        return maos_
