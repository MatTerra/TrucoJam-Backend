from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class NotWaitingForPlayersException(NovaAPIException):
    status_code: int = field(default=412, init=False)
    message: str = field(default="The game is not waiting for players",
                         init=False)
    error_code: int = field(default=41202, init=False)
