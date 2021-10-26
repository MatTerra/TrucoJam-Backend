from dataclasses import dataclass, field

from nova_api import NovaAPIException


@dataclass
class WrongPasswordException(NovaAPIException):
    status_code: int = field(default=403, init=False)
    message: str = field(default="Passwords don't match", init=False)
    error_code: int = field(default=40301, init=False)
