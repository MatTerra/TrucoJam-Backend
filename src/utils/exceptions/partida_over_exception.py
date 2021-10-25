from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class PartidaOverException(NovaAPIException):
    status_code: int = field(default=410, init=False)
    message: str = field(default="Partida is already over", init=False)
    error_code: int = field(default=41002, init=False)
