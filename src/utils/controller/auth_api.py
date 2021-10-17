"""
Anonymous authentication module
"""
from datetime import datetime, timedelta
from os import environ
from uuid import uuid4

from flask import Response
from jose import jwt
from nova_api import success_response

from utils.controller import TRUCOJAM_BASE_CLAIMS


def auth(name: str) -> Response:
    """
    Generates token for anonymous player. Accepts only name and generates \
    a random ID for player identification. The token is valid for a day.

    :param name: Anonymous player nickname
    :return: Success response with valid signed JWT token.
    """
    return success_response(
        201,
        "Anonymous user created",
        {
            "token": __sign_token(__generate_token_claims(name))
        }
    )


def __sign_token(claims: dict) -> str:
    """
    Signs a JWT token with the given claims

    :param claims: Claims to include and sign in token
    :return: The signed token string
    """
    key = environ.get(
        "JWT_SYMM",
        "secretkeysecretkeysecretkeysecretkeysecretkeysecretkeysecretkey"
        "secretkey")

    token = jwt.encode(claims,
                       key,
                       algorithm="HS256")
    return token


def __generate_token_claims(name: str) -> dict:
    """
    Generates the base token claims with the given name for an anonymous \
    player
    :param name: The anonymous player nickname
    :return: The claims dictionary with all necessary claims.
    """
    claims = TRUCOJAM_BASE_CLAIMS.copy()
    claims['iat'] = datetime.now().timestamp()
    claims['exp'] = (datetime.now() + timedelta(days=1)).timestamp()
    claims['name'] = name
    claims['sub'] = uuid4().hex
    claims['kid'] = "symmetric"
    return claims
