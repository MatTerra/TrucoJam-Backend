from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class FullTeamException(NovaAPIException):
    status_code: int = field(default=412, init=False)
    message: str = field(default="Team is already full", init=False)
    error_code: int = field(default=41205, init=False)
