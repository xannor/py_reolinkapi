"""Security Typings"""

from enum import Enum, auto
from typing import Callable, Protocol


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
