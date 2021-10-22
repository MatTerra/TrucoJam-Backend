from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class PartidaOngoingException(NovaAPIException):
    status_code: int = field(default=412, init=False)
    message: str = field(default="The game already has a partida in progress",
                         init=False)
    error_code: int = field(default=41206, init=False)