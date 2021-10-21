"""
Truco JAM Partida backend controller
"""
from copy import deepcopy

from nova_api.auth import validate_jwt_claims
from nova_api import error_response, success_response, use_dao

from utils.database.game_dao import GameDAO
from utils.entity.game import Game
from utils.controller import TRUCOJAM_BASE_CLAIMS


@use_dao(GameDAO, "Unable to list partida")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=True)
def read(id_: str, token_info: dict = None, dao: GameDAO = None):
    """
    Retrieve partida in progress. This only returns if player is \
    a member of the game. May return Gone if game is over.

    :param id_: ID of the game to select the current partida from.
    :param token_info: The user token claims.
    :param dao: The database connection to use.
    :return: The current partida if successful and player in game.
    """
    game = dao.get(id_=id_)
    user_id_ = token_info.get("sub")

    if not game:
        return error_response(404, "This game doesn't exist", {"id_": id_})

    current_partida = game.get_current_partida(user_id_)

    if not current_partida:
        return success_response(204, "No current partida", {})

    return success_response(200, "Current partida retrieved",
                            {"partida": dict(current_partida)})


@use_dao(GameDAO, "Unable to play card")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=True)
def play(id_: str, card: dict, token_info: dict = None, dao: GameDAO = None):
    """
    Play a card from the player hand in the current partida. Only the card \
    id_ must be passed in the card dict. Only works if it is the players turn.

    :param id_: The game in which to play a card
    :param card: A dict with the card ID to play (`{"id_": "..."}`)
    :param token_info: The user token claims
    :param dao: The database connection to use.
    :return: The partida after the card being played. (May include AI plays)
    """
    game: Game = dao.get(id_=id_)
    user_id_ = token_info.get("sub")
    card_id_ = card.get("id_")

    if not game:
        return error_response(404, "This game doesn't exist", {"id_": id_})

    if not game.get_current_partida(user_id_):
        return error_response(400, "No current partida", {})

    partida = game.play(user_id_, card_id_)

    return success_response(200, "Card played", {"partida": dict(partida)})


@use_dao(GameDAO, "Unable to raise partida")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=False)
def raise_(id_: str, token_info: dict = None, dao: GameDAO = None):
    """
    Raises the stakes for the current partida by 3 points. The player may \
    not raise if the other player hasn't decided to fold or go.

    :param id_: The Game in which to raise the partida stakes
    :param token_info: The user token claims
    :param dao: The database connection to use.
    :return: The partida after raise
    """
    pass


@use_dao(GameDAO, "Unable to fold partida")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=False)
def fold(id_: str, token_info: dict = None, dao: GameDAO = None):
    """
    Give up on the current partida after a raise. May only be issued \
    after a raise.

    :param id_: The Game in which to fold the partida
    :param token_info: The user token claims
    :param dao: The database connection to use.
    :return: The partida after fold
    """
    pass
