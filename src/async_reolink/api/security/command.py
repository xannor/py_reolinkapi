"""Security Commands"""

from typing import Protocol, Sequence, TypeGuard

from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from .typing import UserInfo


class LoginRequest(CommandRequest, Protocol):
    """Login Request"""

    user_name: str
    password: str


class LoginResponse(CommandResponse, Protocol):
    """Login Response"""


class LogoutRequest(CommandRequest, Protocol):
    """Logout Request"""


class GetUserRequest(CommandRequest, Protocol):
    """Get User(s) Request"""


class GetUserResponse(CommandResponse, Protocol):
    """Get User(s) Response"""

    users: Sequence[UserInfo]


class CommandFactory(WithCommandFactory, Protocol):
    """Security Command Factory"""

    def create_login_request(self, username: str, password: str) -> LoginRequest:
        """create LoginRequest"""

    def is_login_response(self, response: CommandResponse) -> TypeGuard[LoginResponse]:
        """is LoginResponse"""

    def create_logout_request(self) -> LogoutRequest:
        """create LogoutRequest"""

    def create_get_user_request(self) -> GetUserRequest:
        """create GetUserRequest"""

    def is_get_user_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetUserResponse]:
        """is GetUserResponse"""
