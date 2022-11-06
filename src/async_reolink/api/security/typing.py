"""Security Typings"""

from enum import Enum, auto
from typing import Callable, Protocol


class AuthenticationId(Protocol):
    """Authentication ID"""

    weak: int
    strong: int


class LevelTypes(Enum):
    """User Level Types"""

    GUEST = auto()
    USER = auto()
    ADMIN = auto()


class UserInfo(Protocol):
    """User Record"""

    user_name: str
    level: LevelTypes


class WithSecurity(Protocol):
    """Security Part"""

    _logout_callbacks: list[Callable[[], None]]

    authentication_id: AuthenticationId

    def _create_authentication_id(
        self, username: str, password: str | None = None
    ) -> AuthenticationId:
        ...
