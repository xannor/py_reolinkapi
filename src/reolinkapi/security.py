"""Security"""

from abc import ABC
from dataclasses import dataclass
import inspect
from time import time
from typing import Callable, Final, Iterable, TypedDict
from typing_extensions import TypeGuard

from .system import UserInfo

from .const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from .commands import (
    CommandRequestTypes,
    CommandRequest,
    CommandRequestWithParam,
    CommandResponseType,
)

from .errors import ErrorCodes

from . import connection

LOGOUT_CALLBACK_TYPE = Callable[[], None]


@dataclass
class LoginInfo(UserInfo):
    """Login info"""

    password: str


class LoginTokenType(TypedDict):
    """Login Token"""

    leaseTime: int
    name: str


class LoginTokenV2(LoginTokenType):
    """Login Token V2"""

    checkBasic: int
    countTotal: int


class DigestInfo(TypedDict):
    """Encryption Digest"""

    Cnonce: str
    Method: str
    Nc: str
    Nonce: str
    Qop: str
    Realm: str
    Response: str
    Uri: str
    UserName: str


class Security(ABC):
    """Abstract Security Mixin"""

    def __init__(self) -> None:
        self._logout_callbacks: list[LOGOUT_CALLBACK_TYPE] = []
        self.__token = ""
        super().__init__()
        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.logout)
        self.__last_pwd_hash = 0
        self.__token_expires: float = 0
        self.__auth_failed = False

    @property
    def authenticated(self):
        """authentication status"""
        # we use a 1s offest to give time for simple checks to do an operation
        return not self.__auth_failed and self.authentication_timeout > 1

    @property
    def authentication_required(self):
        """Authentication is missing or invalid"""
        return self.__auth_failed

    @property
    def _auth_failed(self):
        return self.__auth_failed

    @_auth_failed.setter
    def _auth_failed(self, value: bool):
        self.__auth_failed = value

    @property
    def _auth_token(self):
        return self.__token

    @property
    def authentication_timeout(self):
        """authnetication token time remaining"""
        return self.__token_expires - time()

    @property
    def authentication_id(self):
        """authentication id"""
        return self.__last_pwd_hash

    async def _prelogin(self, username: str):
        # keep hash of username so we can logout on new info provided
        pwd_hash = hash(username)
        if self.__last_pwd_hash != pwd_hash:
            await self.logout()
            self.__last_pwd_hash = pwd_hash

        if isinstance(self, connection.Connection):
            if not self._ensure_connection():
                return False
        return True

    async def _do_login(self, username: str, password: str):
        if isinstance(self, connection.Connection):
            return await self._execute(LoginCommand(LoginInfo(username, password)))
        return []

    def _process_token(self, responses: Iterable[CommandResponseType]):
        token = next(map(LoginCommand.get_response, filter(
            LoginCommand.is_response, responses)), None)
        self.__auth_failed = True
        if token is None:
            return False
        self.__auth_failed = False

        self.__token = token["name"]
        self.__token_expires = time() + token["leaseTime"]

        return True

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        if not self._prelogin(username):
            return False

        return self._process_token(await self._do_login(username, password))

    async def logout(self) -> None:
        """Clear authentication information"""

        if self.authenticated:
            if isinstance(self, connection.Connection):
                if self._ensure_connection():
                    errors = list(
                        filter(
                            LogoutCommand.is_error,
                            await self._execute(LogoutCommand()),
                        )
                    )
                    if len(errors) > 0:
                        raise errors[0]

        for callback in self._logout_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        self.__auth_failed = False
        self.__token = ""
        self.__token_expires = 0


class LoginResponseValueType(TypedDict):
    """Authentication Login Response Value Token"""

    Token: LoginTokenType


@dataclass
class LoginRequestParameter:
    """Login Request Parameter"""

    User: LoginInfo


class LoginCommand(CommandRequestWithParam[LoginRequestParameter]):
    """Login Request"""

    COMMAND: Final = "Login"
    RESPONSE: Final = "Token"

    def __init__(self, login: LoginInfo, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY) -> None:
        super().__init__(type(self).COMMAND, action, LoginRequestParameter(login))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[LoginResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, LoginResponseValueType)
        )

    @classmethod
    def get_response(cls, value: LoginResponseValueType):
        """Get Channel Status Response"""
        return value[cls.RESPONSE]

    @classmethod
    def is_auth_failure(cls, value: CommandResponseType):
        return super()._is_response_code(value) and super()._get_response_code(value) == ErrorCodes.AUTH_REQUIRED


class LogoutCommand(CommandRequest):
    """Logout Request"""

    COMMAND: Final = "Logout"

    def __init__(self, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)
