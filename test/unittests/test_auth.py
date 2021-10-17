from os import environ

from jose import jwt
from pytest import fixture
from nova_api.dao import is_valid_uuidv4

from test.unittests import *
from utils.controller import TRUCOJAM_BASE_CLAIMS, auth_api


@fixture(autouse=True)
def success_response(mocker):
    mock = mocker.patch("utils.controller.auth_api.success_response")
    mock.side_effect = lambda status_code=200, message="OK", data={}: \
        (status_code, message, data)
    return mock


#
# @fixture(autouse=True)
# def error_response(mocker):
#     mock = mocker.patch("utils.controller.game_api.error_response")
#     mock.side_effect = lambda status_code=500, message="Error", data={}: \
#         (status_code, message, data)
#     return mock


key = environ.get(
    "JWT_SYMM",
    "secretkeysecretkeysecretkeysecretkeysecretkeysecretkeysecretkey"
    "secretkey")


class TestAuth:
    def test_should_contain_base_claims(self):
        res = auth_api.auth("Teste")
        token = jwt.decode(res[2]["token"], {"symmetric": key},
                           algorithms=['RS256', 'HS256'],
                           options={'verify_aud': False, 'verify_iss': False,
                                    'verify_sub': False, 'verify_jti': False,
                                    'verify_at_hash': False}
                           )
        for claim in TRUCOJAM_BASE_CLAIMS:
            assert token[claim] == TRUCOJAM_BASE_CLAIMS[claim]
        assert token['kid'] == "symmetric"

    def test_should_contain_name(self):
        res = auth_api.auth("Teste")
        token = jwt.decode(res[2]["token"], {"symmetric": key},
                           algorithms=['RS256', 'HS256'],
                           options={'verify_aud': False, 'verify_iss': False,
                                    'verify_sub': False, 'verify_jti': False,
                                    'verify_at_hash': False}
                           )

        assert token["name"] == "Teste"

    def test_should_contain_sub_id(self):
        res = auth_api.auth("Teste")
        token = jwt.decode(res[2]["token"], {"symmetric": key},
                           algorithms=['RS256', 'HS256'],
                           options={'verify_aud': False, 'verify_iss': False,
                                    'verify_sub': False, 'verify_jti': False,
                                    'verify_at_hash': False}
                           )

        assert is_valid_uuidv4(token['sub'])


