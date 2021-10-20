from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class NotUserTurnException(NovaAPIException):
    status_code: int = field(default=412, init=False)
    message: str = field(default="This is not the player's turn",
                         init=False)
    error_code: int = field(default=41204, init=False)
