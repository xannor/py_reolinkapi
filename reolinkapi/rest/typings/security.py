"""Security Typings"""

from typing import TypedDict

from .system import UserInfo


class LoginInfo(UserInfo):
    """Login info"""

    password: str


class LoginToken(TypedDict):
    """Login Token"""

    leaseTime: int
    name: str
