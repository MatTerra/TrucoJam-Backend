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
        "JWT_SYMM_PRIV",
        """-----BEGIN PRIVATE KEY-----
MIIJRAIBADANBgkqhkiG9w0BAQEFAASCCS4wggkqAgEAAoICAQDc2g80LqF7JwzX
5ITJEUmf2lYBQrwJOv3Ce+QfpxjkPLyF49qRj0lGxhar5wTafiNKz5k4qBTegah6
n7gFId9/4Hhxsvd+rW0nLVj5uTyUlRaHNy+nvInmobGu7aJFVMti3hIpd6zuYhEI
1KnG+wK4PRc3ZQ1MMeoUOssAKjPyYbDppCQBmV+Ftnztgjh4snK1c3sd87Lozs0/
XWyEpSOq2J+bSh8N4M3B7pEQLFHVvwPbpqOysc9e33yANlM8BKvRhBdTSUtqa2Vo
lTLhZdFoyZ1l1L6qEa6hhK5grymQFHsRZMccQyHYImRMhVvVcHnUSSxIqFbnFnAE
+psw6tXtGMIovGVoE9c3qE0K98BHc5vWOhafzoAn4krfSNnoeCCKRFNSH8kaUpaS
sz9dhk2Aaqwh69NYI4aNCqG/N6WNRgTsIGvV/3sJxyEhdJV7W7qzo36EqhTPobwT
4dkEXSsY7MrIJDoAF5DonpsM+WB8u7ciZ/n+vVnuozUHi6rvAGL/gdkIm53bYm0b
m+gkdsAOTZ1AM2hfSCLdsQSwPhNBzXlSJe28xEDvHwn8LqO8Jy3uiXIjA5IyI8ME
jsx5sAlumFqMgfm9gY1QPkk052clfZYNA++Dpi6+C4oOHNs60WPLWbs8y29K1KPE
qzx34lplcKQzgXX0dsX4Hie7lW710QIDAQABAoICAEigrT9L1m7ZeK/GxqQYu02G
T6I6f/vJGopKk8qU+OqVzql5NPeJV1+e5PXDEyWHNbP0cT7gh3xkxzMMM0f8y7MR
7on1gM532d14XDpDYFi8bpwo2dMffXoK0pPkMej66aepv+9DG+uI9HEi/nIhOdO8
w1XENYtJHuFoNDnppwuedL9g6zZbab5fNNYmbMvEY1SolWRUMBG/cF/WKUm1xPT6
KAK5bVzzALc17R6UdJUGLA6fzlWFg9x/QkInm1excY+FEOaiw9pLVx39cq4M/cCo
DMrgG5NyHSugpnfFIrXvBknCCniQ2yBorvM7J+gZBPd62MVMFsgH6O66Oy7rC05A
3L+wY8gR7xGyQGw/qXfIhOiQ5X2CtR2FS825pnnX6ESKNpTSP+5fObHdrr1NGNmE
n1dEfp7pYZoYl2xQIYp1Ze7iePjoe5+X9QXoZYwBOyWSIuz7Jln8P1fvYqRECUN2
+4OThMZkuHFO8lQYHIZO5WGludRMzY82hvH8zkzJX6mBQfixs0MUuIbwxuixB7BI
3duLL2MUZUJqbzVPuLSaEJJS05L5ZnVR4x8bVFA2ANYrWZmpYh2+LGfv9jRPG5nQ
w+l3IhfUTLaMHwNNdXeNF7Su8mmBka/WPOC0Qqy6+Q9pigJVCzGDwUQhHdA9bqa3
deI6e4w8jV3NouJ7xXHBAoIBAQDxyMNhuEpJJtM6PseDZ7rOiz1HxqHT14CzQG8G
CHNMmwTa3kmCBK0feUytQlfN8f6SGhta9pHtTUk2+WRoYD+t0wKjN173Fa+WoFF2
H3KvLCbCSGEFBBZ3PoeIc2+LqfqiOfiKMILNa902AEGn82dlTNshxcR7Ue1JulVP
g51I8YTfVGEyLY39Sb0fSNKKwnebHJNU9fRLmO6YzCi4w87P1MMJu9JU2bEgrOzW
OdyWAH38XqyYqUxgUpCYyvtxYWgRr/qzA3ZtG6RN0rww0EQtUawiiVSN6V7tWpUr
3ky1HfgzsvC2kPTIyvirA6UQYGqEMnIObx7DjDun3JTWhN7TAoIBAQDp1jrRCZI5
yN2q2OBvt3yoJRw0F/IZOdmdKQBBcBwOCdbqLifetWeyu8OPY4Uauzb+2w3urZnV
q9Mx58YZap4YGGTsSsGEEN+QPAn9kJbAng3EaadfqCI73UjlVudpYp70GqnK+KWo
bJ9fDxHktYMNS90X4pOA6pgzxp2qMLU2cK9Er61zLerac9AHAXbjPmF546PUPo3p
PpesodI5UCh1H8Fu/NKGSZv4XyOCX9qA0hHzU6P+oVpzr9uVGfWIxxaImANUDRih
mUN+74qeuozmar9yg7tOTYbvSBjC9I5aKTGS0f3Klmsnj7koTMNK3NpaJQy0nvyQ
haJLVWmo9tpLAoIBAQDWUy7Ourwu6BmpsejNlO/FEyx5KZxd2tQdEWrZIDiEmY3O
LelfNaH5Gl9b3klTJ8aP4FCLa7KjdjUGZEAbPeZ0wW2/HOAziqehj+9mFC5nFW4u
HlbSSXNYtLcTv7ALT9v6XgTxCluImKr4qXWJ2Xu4Ek7VOygWYONEzcW9vF96P42X
IoceIb+R3QGmb7kig4velZAMahHpyWEHVUJrtjbniCRzxmiGCoq2+lLe+1+MIFeN
lKbOlJQ9djLzHkuRj9TeiO5kLReXVD9rNPjZFGS6/4DlBHNNcKdTI07EGkRI8I4J
1f8G9qvmKfYQMiTpxW3mTYlJPjs5AGAJRsEw/4s9AoIBAQDoDnAELulsawiAmgXx
GDifbWSV1gWuPxjUvHHCfw14aQ9dCz0J6SDl4Sxryim3o38qYB1tdd6qi4BlkEup
wYLvCpZtYKq28z/KFascdjcFJFUpTGiLp4GBw1KqNholHXf9a9CA200a3eEzJvNs
8y0BLv5Uy8fyMd2l1D93PCs5wY5OLcGGAlWFQVV6/lsLnUaC/gQBh6qxhCplaZoE
wqXDxiXijQgnuDkOvOuyYImpOdASmDixY1MuZ6EUUNS4Tkrwd1smOHDvPfgbqoD4
kM1vhRRFArIJPSrhn7zjDGuQ0jyeJcMlHy1r71eixLsyOgZ/WzFGtliS2+t5s2PO
CFwNAoIBAQCwJ55715XDoE3Bb5mNA//n0usHaxtOjytwLQ8hO8dqJmPzp7y4Cz84
IovEM5gJrmITq7+D05fWDl648m/jx6TDXfMZlWl+hNl/2CbglJ8VvdBDuHPk1y3W
p3qgf3v9pQR75Anx0dxpN5Qz0kBZwvDmjf5MR8Ss2qyfniD1CJu1PCMtPERRrQpy
JuXi+7hzB6d4v5KQYBeSLfU7r+Jsm1hmRncVQ1QAfurFRqmcJYF8ByugNXg+Sap1
TEqwKdvpiZZqDqZqEwbh+BMKbQGEEx/MWosPU7Cp1umALnyuon58C3ht7x7yErsW
ESJs4ho6Blqz5qB//KMmGKSEXRV7Okfp
-----END PRIVATE KEY-----
""")

    token = jwt.encode(claims,
                       key,
                       algorithm="RS256")
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
