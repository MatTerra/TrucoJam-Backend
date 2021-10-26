from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class GameOverException(NovaAPIException):
    status_code: int = field(default=410, init=False)
    message: str = field(default="Game is already over", init=False)
    error_code: int = field(default=41001, init=False)
