from dataclasses import fields

from nova_api import error_response, success_response, use_dao
from nova_api.dao.mongo_dao import MongoDAO

from utils.database.game_dao import GameDAO
from utils.entity.game import Game


@use_dao(GameDAO, "API Unavailable")
def probe(dao: MongoDAO = None):
    total, _ = dao.get_all(length=1, offset=0, filters=None)
    return success_response(message="API Ready",
                            data={"available": total})


@use_dao(GameDAO, "Unable to list game")
def read(length: int = 20, offset: int = 0,
         dao: MongoDAO = None, **kwargs):
    filters = dict()

    entity_attributes = [field.name for field in fields(Game)]

    for key, value in kwargs.items():
        if key not in entity_attributes:
            continue

        filters[key] = value.split(',') \
                       if len(str(value).split(',')) > 1 \
                       else value

    total, results = dao.get_all(length=length, offset=offset,
                                 filters=filters if filters else None)
    return success_response(message="List of game",
                            data={"total": total, "results": [dict(result)
                                                              for result
                                                              in results]})


@use_dao(GameDAO, "Unable to retrieve game")
def read_one(id_: str, dao: MongoDAO = None):
    result = dao.get(id_=id_)

    if not result:
        return success_response(status_code=404,
                                message="Game not found in database",
                                data={"id_": id_})

    return success_response(message="Game retrieved",
                            data={"Game": dict(result)})


@use_dao(GameDAO, "Unable to create game")
def create(entity: dict, dao: MongoDAO = None):
    entity_to_create = Game(**entity)

    dao.create(entity=entity_to_create)

    return success_response(message="Game created",
                            data={"Game": dict(entity_to_create)})


@use_dao(GameDAO, "Unable to update game")
def update(id_: str, entity: dict, dao: MongoDAO = None):
    entity_to_update = dao.get(id_)

    if not entity_to_update:
        return error_response(status_code=404,
                              message="Game not found",
                              data={"id_": id_})

    entity_fields = dao.fields.keys()

    for key, value in entity.items():
        if key not in entity_fields:
            raise KeyError("{key} not in {entity}"
                           .format(key=key,
                                   entity=dao.return_class))

        entity_to_update.__dict__[key] = value

    dao.update(entity_to_update)

    return success_response(message="Game updated",
                            data={"Game": dict(entity_to_update)})


@use_dao(GameDAO, "Unable to delete game")
def delete(id_: str, dao: MongoDAO):
    entity = dao.get(id_=id_)

    if not entity:
        return error_response(status_code=404,
                              message="Game not found",
                              data={"id_": id_})

    dao.remove(entity)

    return success_response(message="Game deleted",
                            data={"Game": dict(entity)})
