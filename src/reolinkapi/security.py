"""Security"""

from abc import ABC
from dataclasses import dataclass
import inspect
from time import time
from typing import Callable, Final, Iterable, TypedDict

from .system import UserInfo

from .const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from .commands import COMMAND, COMMAND_RESPONSE_VALUE, CommandRequest, CommandRequestTypes, CommandRequestWithParam, CommandResponse, create_value_has_key, iserror, isvalue

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
            return await self._execute(LoginRequest(LoginInfo(username, password)))
        return []

    def _process_token(self, responses: Iterable[CommandResponse]):
        token = next(LoginRequest.get_responses(responses), None)
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
                            iserror,
                            await self._execute(LogoutRequest()),
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

class LoginResponseValue(TypedDict):
    """Authentication Login Response Value Token"""

    Token: LoginTokenType

@dataclass
class LoginRequestParameter:
    """Login Request Parameter"""

    User: LoginInfo

class LoginRequest(CommandRequestWithParam[LoginRequestParameter]):
    """Login Request"""

    COMMAND:Final = "Login"
    RESPONSE:Final = "Token"

    def __init__(self, login:LoginInfo, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY)->None:
        super().__init__(type(self).COMMAND,action, LoginRequestParameter(login))

    @classmethod
    def has_auth_failure(cls, responses: Iterable[CommandResponse]):
        """Check responses for auth failure"""
        return (
            next(
                (
                    error
                    for error in filter(iserror, responses)
                    if error["error"]["rspCode"] == ErrorCodes.AUTH_REQUIRED
                ),
                None,
            )
            is not None
        )

    @classmethod
    def get_responses(cls, responses: Iterable[CommandResponse]):
        """Get Responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _istoken,
                filter(
                    isvalue,
                    filter(lambda response: response[COMMAND] == cls.COMMAND, responses),
                ),
            ),
        )



_istoken = create_value_has_key(LoginRequest.RESPONSE, LoginResponseValue)

class LogoutRequest(CommandRequest):
    """Logout Request"""

    COMMAND:Final = "Logout"

    def __init__(self, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init(type(self).COMMAND, action)
