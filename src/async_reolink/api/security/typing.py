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
