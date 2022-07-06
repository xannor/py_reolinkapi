"""Security"""

from abc import ABC
from dataclasses import dataclass
import inspect
from time import time
from typing import Callable, Final, AsyncIterable, TypedDict
from typing_extensions import TypeGuard

from .system import User

from .const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from .utils import anext

from .commands import (
    CommandRequestTypes,
    CommandRequest,
    CommandRequestWithParam,
    CommandResponseType,
    CommandResponseValue,
)

from .errors import ErrorCodes

from . import connection


@dataclass
class Login(User):
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
        self._logout_callbacks: list[Callable[[], None]] = []
        self.__token = ""
        super().__init__()
        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.logout)
        self.__last_pwd_hash = 0
        self.__token_expires: float = 0

    @property
    def is_authenticated(self):
        """authentication status"""
        # we use a 1s offest to give time for simple checks to do an operation
        return bool(self.__token) and self.authentication_timeout > 1

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
            if not self.is_connected:
                return False
        return True

    async def _process_token(self, responses: AsyncIterable[CommandResponseType]):
        async for response in responses:
            if not LoginCommand.is_response:
                continue
            token = LoginCommand.get_value(response)

            self.__token = token["name"]
            self.__token_expires = time() + token["leaseTime"]

            return True

        return False

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        if not isinstance(self, connection.Connection):
            return False

        if not await self._prelogin(username):
            return False

        responses = connection.async_trap_errors(await self._execute(LoginCommand(  # pylint: disable=no-member
            Login(username, password))))

        return await self._process_token(responses)

    async def logout(self) -> None:
        """Clear authentication information"""

        if not self.is_authenticated:
            return

        if not isinstance(self, connection.Connection):
            return

        if not self.is_connected:  # pylint: disable=no-member
            return

        responses = connection.async_trap_errors(await self._execute(  # pylint: disable=no-member
            LogoutCommand()))

        try:
            await anext(responses)

            for callback in self._logout_callbacks:
                if inspect.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
        finally:
            self.__token = ""
            self.__token_expires = 0


class LoginResponseValueType(TypedDict):
    """Authentication Login Response Value Token"""

    Token: LoginTokenType


@ dataclass
class LoginRequestParameter:
    """Login Request Parameter"""

    User: Login


class LoginCommand(CommandRequestWithParam[LoginRequestParameter]):
    """Login Request"""

    COMMAND: Final = "Login"
    RESPONSE: Final = "Token"

    def __init__(
        self,
        login: Login,
        action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ) -> None:
        super().__init__(type(self).COMMAND, action, LoginRequestParameter(login))

    @ classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[LoginResponseValueType]]:
        """Is response a search result"""
        return cls._is_response(value, command=cls.COMMAND) and cls._is_typed_value(
            value, cls.RESPONSE, LoginResponseValueType
        )

    @ classmethod
    def get_value(cls, value: CommandResponseValue[LoginResponseValueType]):
        """Get Channel Status Response"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]

    @ classmethod
    def is_auth_failure(cls, value: CommandResponseType):
        """is authentication failure response"""
        return (
            cls._is_response_code(value)
            and cls._get_response_code(value) == ErrorCodes.AUTH_REQUIRED
        )


class LogoutCommand(CommandRequest):
    """Logout Request"""

    COMMAND: Final = "Logout"

    def __init__(self, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)
