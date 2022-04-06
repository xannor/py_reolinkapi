""""Security helpers"""

from typing import Final, Iterable, TypedDict

from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME


from . import commands as commandHelpers
from ..typings.commands import (
    COMMAND,
    COMMAND_RESPONSE_VALUE,
    CommandRequest,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)
from ..typings.security import LoginInfo, LoginToken
from ..models.errors import ErrorCodes


class LoginResponseValue(TypedDict):
    """Authentication Login Response Value Token"""

    Token: LoginToken


LOGIN_VALUE: Final = "Token"

_istoken = commandHelpers.create_value_has_key("Token", LoginResponseValue)


class LoginRequestCommandParameter(TypedDict):
    """Login Request Command Parameter"""

    User: LoginInfo


LOGIN_COMMAND: Final = "Login"

LOGOUT_COMMAND: Final = "Logout"


def has_auth_failure(responses: Iterable[CommandResponse]):
    """check responses for auth failure"""
    return (
        next(
            (
                error
                for error in filter(commandHelpers.iserror, responses)
                if error["error"]["rspCode"] == ErrorCodes.AUTH_REQUIRED
            ),
            None,
        )
        is not None
    )


def create_login(username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD):
    """Create Login Request"""
    return CommandRequestWithParam(
        cmd=LOGIN_COMMAND,
        action=CommandRequestTypes.VALUE_ONLY,
        param=LoginRequestCommandParameter(
            User=LoginInfo(userName=username, password=password)
        ),
    )


def login_responses(responses: Iterable[CommandResponse]):
    """Get Login Responses"""

    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE][LOGIN_VALUE],
        filter(
            _istoken,
            filter(
                commandHelpers.isvalue,
                filter(lambda response: response[COMMAND] == LOGIN_COMMAND, responses),
            ),
        ),
    )


def create_logout():
    """Create Login Request"""
    return CommandRequest(cmd=LOGOUT_COMMAND, action=CommandRequestTypes.VALUE_ONLY)
