from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class InvalidTeamException(NovaAPIException):
    status_code: int = field(default=412, init=False)
    message: str = field(default="team index out of range",
                         init=False)
    error_code: int = field(default=41202, init=False)
















