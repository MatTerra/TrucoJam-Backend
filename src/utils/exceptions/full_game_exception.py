from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class FullGameException(NovaAPIException):
    status_code: int = field(default=412, init=False)
    message: str = field(default="Game is already full", init=False)
    error_code: int = field(default=41202, init=False)
