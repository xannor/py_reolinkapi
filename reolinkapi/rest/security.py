""" Security Commands """

from dataclasses import dataclass, field
import time
from typing import ClassVar, Optional

from .command import response_type

from ..utils.dataclasses import keyword
from .exceptions import ErrorCodes, ResponseError

from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from ..meta.connection import ConnectionInterface
from .command import (
    CommandRequest,
    CommandRequestParameter,
    CommandError,
    CommandValueResponse,
    CommandValueResponseValue,
)


@dataclass
class LoginInfo:
    """Login info"""

    username: str = field(metadata=keyword("userName"))
    password: str = field()


@dataclass
class LoginToken:
    """Login Token"""

    leasetime: int = field(metadata=keyword("leaseTime"))
    value: str = field(metadata=keyword("name"))


def _create_invalid_token():
    return LoginToken(0, "")


@dataclass
class LoginResponseValue(CommandValueResponseValue):
    """Authentication Login Response Value Token"""

    token: LoginToken = field(
        default_factory=_create_invalid_token, metadata=keyword("Token")
    )


@dataclass
class LoginResponse(CommandValueResponse):
    """Authentication Login Response"""

    value: LoginResponseValue = field(default_factory=LoginResponseValue)


@dataclass
class LoginRequestParameter(CommandRequestParameter):
    """Login Parameter"""

    info: LoginInfo = field(metadata=keyword("User"))


@dataclass
@response_type(LoginResponse)
class LoginRequest(CommandRequest):
    """Authentication Login Request"""

    COMMAND: ClassVar = "Login"
    param: LoginRequestParameter = field()

    def __post_init__(self):
        self.command = type(self).COMMAND


@dataclass
class LogoutResponse(CommandValueResponse):
    """Logout Response"""


@dataclass
@response_type(LogoutResponse)
class LogoutRequest(CommandRequest):
    """Logout Request"""

    COMMAND: ClassVar = "Logout"

    def __post_init__(self):
        self.command = type(self).COMMAND
        self.param = None


class Security:
    """Security mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token: Optional[LoginToken] = None
        self._token_timestamp: float = 0
        self._last_pwd_hash: int = 0
        if isinstance(self, ConnectionInterface) and not hasattr(
            self, "_get_disconnect_callbacks"
        ):
            self._get_disconnect_callbacks().append(self.logout)
            self._ensure_connection = self._ensure_connection
            self._execute = self._execute

    @property
    def authenticated(self):
        """authentication status"""
        # we use a 100ms offest to give time for simple checks to do an operation
        return self.authentication_timeout > 100

    @property
    def authentication_timeout(self):
        """authnetication token time remaining"""
        if self._token is None:
            return 0
        rem = (self._token_timestamp + self._token.leasetime) - time.time()
        if rem > 0:
            return rem
        return 0

    def _get_auth_token(self):
        return self._token.value if self.authenticated else None

    @property
    def token(self):
        return self._get_auth_token()

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        # keep hash of username so we can logout on new info provided
        pwd_hash = hash(username)
        if self._last_pwd_hash != pwd_hash:
            await self.logout()
            self._last_pwd_hash = pwd_hash

        if not self._ensure_connection():
            return False

        request = LoginRequest(LoginRequestParameter(LoginInfo(username, password)))
        results = await self._execute(request)
        if len(results) != 1 or not isinstance(results[0], LoginResponse):
            if isinstance(results[0], CommandError):
                if results[0].error.code == ErrorCodes.LOGIN_FAILED:
                    return False
                raise ResponseError(results[0])
            return False

        self._token = results[0].value.token
        self._token_timestamp = time.time()

        return True

    async def logout(self):
        """Clear authentication information"""
        if self.authenticated:
            if self._ensure_connection():
                results = await self._execute(LogoutRequest())
                if len(results) != 1 or not isinstance(results[0], LogoutResponse):
                    raise ResponseError(results[0])

        self._token = None
        self._token_timestamp = 0
