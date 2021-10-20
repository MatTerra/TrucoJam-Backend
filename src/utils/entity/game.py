"""
Game model module
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from nova_api.entity import Entity

from utils.entity.partida import Partida
from utils.exceptions.full_game_exception import FullGameException
from utils.exceptions.not_waiting_for_players_exception import \
    NotWaitingForPlayersException
from utils.exceptions.user_already_in_game_exception import \
    UserAlreadyInGameException
from utils.exceptions.user_not_in_game_exception import UserNotInGameException
from utils.exceptions.wrong_password_exception import WrongPasswordException


def pontuacao_vazia() -> List[int]:
    """
    Simple empty pontuacao generator

    :return: Empty pontuacao list
    """
    return [0, 0]


def times_vazios() -> List[List[str]]:
    """
    Simple empty times generator

    :return: Empty times list
    """
    return [[], []]


class GameStatus(Enum):
    """
    Game status enumeration
    """
    AguardandoJogadores = 0
    Jogando = 1
    Encerrado = 2


@dataclass
class Game(Entity):
    """
    Game model
    """
    pontuacao: list = field(default_factory=pontuacao_vazia)
    senha: str = ""
    times: list = field(default_factory=times_vazios)
    partidas: list = field(default_factory=list)
    jogadores: list = field(default_factory=list)
    status: GameStatus = GameStatus.AguardandoJogadores

    def join(self, user_id_: str, senha: str = "") -> None:
        """
        Join game and updates the status if game full after join.

        :raise FullGameException: If the game already has 4 players.
        :raise NotWaitingForPlayersException: If the game is not in the \
        waiting state.
        :raise UserAlreadyInGameException: If user is already participating \
        in this game.
        :raise WrongPasswordException: If the senha informed doesn't match \
        the game senha.

        :param user_id_: User joining the game.
        :param senha: Senha of the game.
        """
        if len(self.jogadores) == 4:
            raise FullGameException(f"Game {self.id_} is already full.")

        if self.status != GameStatus.AguardandoJogadores:
            raise NotWaitingForPlayersException(f"Game {self.id_} not "
                                                f"waiting for players.")

        if user_id_ in self.jogadores:
            raise UserAlreadyInGameException(f"User {user_id_} "
                                             f"already in game.")

        if self.senha and senha != self.senha:
            raise WrongPasswordException(f"Incorrect password: {senha} "
                                         f"for game {self.id_}.")

        self.jogadores.append(user_id_)

        if len(self.jogadores) == 4:
            self.status = GameStatus.Jogando

    def get_current_partida(self, user_id_: str) -> Optional[Partida]:
        """
        Returns the current partida correctly formatted for the player, that
        is, excludes other players cards.

        :raise UserNotInGameException: If user is not a player in this game.

        :param user_id_: The player user_id_ to get the partida for.
        :return: The partida viewed by the player.
        """
        if user_id_ not in self.jogadores:
            raise UserNotInGameException(f"User {user_id_} not found in "
                                         f"game {self.id_}")

        if len(self.partidas) > 0:
            partida = Partida(**self.partidas[-1])
            Game.__filter_hands(partida, user_id_)
            return partida

        return None

    @staticmethod
    def __filter_hands(partida, user_id_):
        partida.maos = [mao for mao in partida.maos
                        if mao.get("jogador") == user_id_
                        or Game.__hand_has_played_cards(mao)]
        Game.__filter_played_cards(partida.maos, user_id_)

    @staticmethod
    def __filter_played_cards(maos, user_id_):
        for mao in maos:
            if mao.get("jogador") == user_id_:
                continue
            mao["cartas"] = [carta for carta in mao.get("cartas")
                             if carta.get("rodada") is not None]

    @staticmethod
    def __hand_has_played_cards(mao):
        for carta in mao.get("cartas"):
            if carta.get("rodada") is not None:
                return True
        return False
