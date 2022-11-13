"""Security Commands"""

from typing import Protocol, Sequence

from .typing import UserInfo


class LoginRequest(Protocol):
    """Login Request"""

    user_name: str
    password: str


class LoginResponse(Protocol):
    """Login Response"""


class LogoutRequest(Protocol):
    """Logout Request"""


class GetUserRequest(Protocol):
    """Get User(s) Request"""


class GetUserResponse(Protocol):
    """Get User(s) Response"""

    users: Sequence[UserInfo]
