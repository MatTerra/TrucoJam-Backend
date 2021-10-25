from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class InvalidTeamException(NovaAPIException):
    status_code: int = field(default=400, init=False)
    message: str = field(default="Team index out of range",
                         init=False)
    error_code: int = field(default=40001, init=False)
















