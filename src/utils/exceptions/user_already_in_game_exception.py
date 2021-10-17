from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class UserAlreadyInGameException(NovaAPIException):
    status_code: int = field(default=412, init=False)
    message: str = field(default="User is already in game", init=False)
    error_code: int = field(default=41201, init=False)
