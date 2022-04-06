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


class LoginTokenV2(LoginToken):
    """Login Token V2"""

    checkBasic: int
    countTotal: int
