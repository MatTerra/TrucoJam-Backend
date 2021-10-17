"""
Truco JAM Partida backend controller
"""
from copy import deepcopy

from nova_api.auth import validate_jwt_claims
from nova_api.dao.mongo_dao import MongoDAO
from nova_api import error_response, success_response, use_dao

from utils.database.game_dao import GameDAO
from utils.entity.game import Game
from utils.controller import TRUCOJAM_BASE_CLAIMS

@use_dao(GameDAO, "Unable to list partida")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=False)
def read(id_: str, token_info: dict = None, dao: GameDAO = None):
    pass

@use_dao(GameDAO, "Unable to play card")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=False)
def play(id_: str, card: int, token_info: dict = None, dao: GameDAO = None):
    pass

@use_dao(GameDAO, "Unable to raise partida")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=False)
def raise_(id_: str, token_info: dict = None, dao: GameDAO = None):
    pass

@use_dao(GameDAO, "Unable to fold partida")
@validate_jwt_claims(claims=TRUCOJAM_BASE_CLAIMS, add_token_info=False)
def fold(id_: str, token_info: dict = None, dao: GameDAO = None):
    pass
