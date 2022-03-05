""" Security Commands """
from __future__ import annotations

import time
from typing import TypedDict

from . import connection

from .typings.commands import (
    CommandRequest,
    CommandRequestTypes,
    CommandResponseErrorValue,
)

from .typings.security import LoginInfo, LoginToken

from .exceptions import ErrorCodes, CommandError

from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME


class LoginResponseValue(TypedDict):
    """Authentication Login Response Value Token"""

    Token: LoginToken


class LoginRequestCommandParameter(TypedDict):
    """Login Request Command Parameter"""

    User: LoginInfo


LOGIN_COMMAND = "Login"

LOGOUT_COMMAND = "Logout"

CACHE_TOKEN = "token"
CACHE_TOKEN_EXPIRES = "token_expires"


class _LocalCache(TypedDict):
    token: str
    token_expires: int


class Security:
    """Security mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_pwd_hash: int = 0
        self.__cache: _LocalCache = (
            getattr(self, "__cache") if hasattr(self, "__cache") else {}
        )
        setattr(self, "__cache", self.__cache)
        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.logout)
            if not hasattr(self, "_execute"):
                self._execute = self._execute
                self._ensure_connection = self._ensure_connection

    @property
    def authenticated(self):
        """authentication status"""
        # we use a 100ms offest to give time for simple checks to do an operation
        return self.authentication_timeout > 100

    @property
    def authentication_timeout(self):
        """authnetication token time remaining"""
        if CACHE_TOKEN_EXPIRES not in self.__cache:
            return 0
        rem = time.time() - self.__cache[CACHE_TOKEN_EXPIRES]
        return rem if rem > 0 else 0

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

        results = await self._execute(
            CommandRequest(
                cmd=LOGIN_COMMAND,
                action=CommandRequestTypes.VALUE_ONLY,
                param=LoginRequestCommandParameter(
                    User=LoginInfo(userName=username, password=password)
                ),
            )
        )
        if (
            len(results) != 1
            or not isinstance(results[0], dict)
            or results[0]["cmd"] != LOGIN_COMMAND
        ):
            return False
        if "error" in results[0]:
            result: CommandResponseErrorValue = results[0]
            if result["error"]["rspCode"] == ErrorCodes.LOGIN_FAILED:
                return False
            raise CommandError(result)

        value: LoginResponseValue = results[0]["value"]
        self.__cache["token"] = value["Token"]["name"]
        self.__cache["token_expires"] = time.time() + value["Token"]["leaseTime"]

        return True

    async def logout(self):
        """Clear authentication information"""

        if self.authenticated:
            if self._ensure_connection():
                results = await self._execute(
                    CommandRequest(
                        cmd=LOGOUT_COMMAND, action=CommandRequestTypes.VALUE_ONLY
                    )
                )
                if (
                    len(results) != 1
                    or not isinstance(results[0], dict)
                    or results[0]["cmd"] != LOGOUT_COMMAND
                ):
                    raise CommandError(results[0])

        self.__cache.pop(CACHE_TOKEN, None)
        self.__cache.pop(CACHE_TOKEN_EXPIRES, None)
