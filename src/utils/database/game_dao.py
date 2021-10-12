"""
Module for database integration for Game entity
"""
from nova_api.dao.mongo_dao import MongoDAO

from utils.entity.game import Game


class GameDAO(MongoDAO):
    """
    DAO class for Game with a Mongo backend
    """
    def __init__(self, **kwargs):
        super().__init__(return_class=Game, **kwargs)
