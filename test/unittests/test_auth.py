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
    "-----BEGIN PUBLIC KEY-----\n"
    "MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA3NoPNC6heycM1+SEyRFJ\n"
    "n9pWAUK8CTr9wnvkH6cY5Dy8hePakY9JRsYWq+cE2n4jSs+ZOKgU3oGoep+4BSHf\n"    
    "f+B4cbL3fq1tJy1Y+bk8lJUWhzcvp7yJ5qGxru2iRVTLYt4SKXes7mIRCNSpxvsC\n"
    "uD0XN2UNTDHqFDrLACoz8mGw6aQkAZlfhbZ87YI4eLJytXN7HfOy6M7NP11shKUj\n"
    "qtifm0ofDeDNwe6RECxR1b8D26ajsrHPXt98gDZTPASr0YQXU0lLamtlaJUy4WXR\n"
    "aMmdZdS+qhGuoYSuYK8pkBR7EWTHHEMh2CJkTIVb1XB51EksSKhW5xZwBPqbMOrV\n"
    "7RjCKLxlaBPXN6hNCvfAR3Ob1joWn86AJ+JK30jZ6HggikRTUh/JGlKWkrM/XYZN\n"
    "gGqsIevTWCOGjQqhvzeljUYE7CBr1f97CcchIXSVe1u6s6N+hKoUz6G8E+HZBF0r\n"
    "GOzKyCQ6ABeQ6J6bDPlgfLu3Imf5/r1Z7qM1B4uq7wBi/4HZCJud22JtG5voJHbA\n"
    "Dk2dQDNoX0gi3bEEsD4TQc15UiXtvMRA7x8J/C6jvCct7olyIwOSMiPDBI7MebAJ\n"
    "bphajIH5vYGNUD5JNOdnJX2WDQPvg6YuvguKDhzbOtFjy1m7PMtvStSjxKs8d+Ja\n"
    "ZXCkM4F19HbF+B4nu5Vu9dECAwEAAQ==\n"
    "-----END PUBLIC KEY-----")


class TestAuth:
    def test_should_contain_base_claims(self):
        res = auth_api.auth("Teste")
        token = jwt.decode(res[2]["token"], {"symmetric": key},
                           algorithms=['RS256'],
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
                           algorithms=['RS256'],
                           options={'verify_aud': False, 'verify_iss': False,
                                    'verify_sub': False, 'verify_jti': False,
                                    'verify_at_hash': False}
                           )

        assert token["name"] == "Teste"

    def test_should_contain_sub_id(self):
        res = auth_api.auth("Teste")
        token = jwt.decode(res[2]["token"], {"symmetric": key},
                           algorithms=['RS256'],
                           options={'verify_aud': False, 'verify_iss': False,
                                    'verify_sub': False, 'verify_jti': False,
                                    'verify_at_hash': False}
                           )

        assert is_valid_uuidv4(token['sub'])
