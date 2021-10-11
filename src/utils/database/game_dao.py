from nova_api.dao.mongo_dao import MongoDAO

from utils.entity.game import Game


class GameDAO(MongoDAO):
    def __init__(self, return_class=Game, **kwargs):
        super().__init__(**kwargs)
