"""
Truco JAM Game backend controller
"""
from copy import deepcopy

from nova_api.auth import validate_jwt_claims
from nova_api.dao.mongo_dao import MongoDAO
from nova_api import error_response, success_response, use_dao

from utils.database.game_dao import GameDAO
from utils.entity.game import Game
from utils.controller import TRUCOJAM_BASE_CLAIMS


@use_dao(GameDAO, "API Unavailable")
def probe(dao: MongoDAO = None):
    """
    Health Check handler

    :param dao: The DAO to use to communicate with the database
    :return: Success Response if ok. Error Response otherwise.
    """
    total, _ = dao.get_all(length=1, offset=0, filters=None)
    return success_response(message="API Ready",
                            data={"available": total})


@use_dao(GameDAO, "Unable to list game")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=False)
def read(length: int = 20, offset: int = 0,
         # pylint: disable=W0613
         dao: MongoDAO = None, token_info: dict = None, **kwargs):
    """
    Lists all Games in the database

    :param length: Amount of games to select
    :param offset: Games to skip while selecting
    :param dao: The DAO to use to communicate with the database
    :param kwargs: Filters to apply to Game selection
    :return:
    """
    filters = dict()

    # entity_attributes = [field.name for field in fields(Game)]

    # for key, value in kwargs.items():
    #     if key not in entity_attributes:
    #         continue
    #
    #     filters[key] = value.split(',', 1) \
    #         if str(value).count(',') >= 1 \
    #            and str(value).split(',')[0] \
    #            in dao.ALLOWED_COMPARATORS \
    #         else value

    total, results = dao.get_all(length=length, offset=offset,
                                 filters=filters if filters else None)
    return success_response(message="List of game",
                            data={"total": total, "results": [dict(result)
                                                              for result
                                                              in results]})


@use_dao(GameDAO, "Unable to retrieve game")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=True)
def read_one(id_: str, dao: MongoDAO = None, token_info: dict = None):
    """
    Recovers a single game from the database

    :param id_: ID of the game to recover
    :param dao: The DAO to use to communicate with the database
    :return:
    """
    result = dao.get(id_=id_)

    if not result:
        return success_response(status_code=404,
                                message="Game not found in database",
                                data={"id_": id_})

    if token_info.get("sub") not in result.jogadores:
        return error_response(403, "Player not in game", {"id_": id_})

    return success_response(message="Game retrieved",
                            data={"Game": dict(result)})


@use_dao(GameDAO, "Unable to create game")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=True)
def create(entity: dict, dao: MongoDAO = None, token_info: dict = None):
    """
    Creates a new game in the database

    :param entity: The fields of the game
    :param dao: The DAO to use to communicate with the database
    :return:
    """
    # TODO Treat n_players
    entity_to_create = Game(**entity) # TODO change to only use senha
    entity_to_create.join(token_info.get("sub"), entity_to_create.senha)

    dao.create(entity=entity_to_create)

    return success_response(status_code=201,
                            message="Game created",
                            data={"Game": dict(entity_to_create)})


@use_dao(GameDAO, "Unable to delete game")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=True)
def delete(id_: str, dao: MongoDAO):
    """
    Endpoint to delete a game

    :param id_: The ID of the game to delete
    :param dao: The DAO to use to communicate with the database
    :return:
    """
    entity = dao.get(id_=id_)

    if not entity:
        return error_response(status_code=404,
                              message="Game not found",
                              data={"id_": id_})

    dao.remove(entity)

    return success_response(message="Game deleted",
                            data={"Game": dict(entity)})


@use_dao(GameDAO, "Unable to start partida")
def start_game(id_: str, dao: MongoDAO):
    """
    Endpoint to create a new partida in a game

    :param id_: ID of the game in which to create the partida
    :param dao: The DAO to use to communicate with the database
    :return:
    """
    dao.get(id_=id_)


@use_dao(GameDAO, "Unable to join game")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=True)
def join(id_: str, password: dict = None, token_info: dict = None,
         dao: GameDAO = None):
    """
    Join a game. This checks the password informed and adds the user \
        to the game if correct.

    :param dao: Database connection
    :param id_: ID of the game to join
    :param password: Dict with the password to join the game
    :param token_info: User token data
    :return: Success if the join was successful and false otherwise.
    """
    game: Game = dao.get(id_=id_)
    user_id_ = token_info.get("sub")
    senha = password.get("senha")

    if not game:
        return error_response(404, "This game doesn't exist", {"id_": id_})

    game.join(user_id_, senha)

    dao.update(deepcopy(game))

    return success_response(message="Joined Game",
                            data={"Game": dict(game)})

@use_dao(GameDAO, "Unable to join team in game")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=True)
def join_team(id_: str, team_id_: str, token_info: dict = None,
              dao: GameDAO = None):
    pass
