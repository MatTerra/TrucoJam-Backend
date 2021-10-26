from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class UserNotInGameException(NovaAPIException):
    status_code: int = field(default=403, init=False)
    message: str = field(default="User is not in game", init=False)
    error_code: int = field(default=40302, init=False)
