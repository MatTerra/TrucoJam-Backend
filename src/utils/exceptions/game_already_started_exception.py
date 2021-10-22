from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class GameAlreadyStartedException(NovaAPIException):
    status_code: int = field(default=410, init=False)
    message: str = field(default="Game already started", init=False)
    error_code: int = field(default=41003, init=False)
