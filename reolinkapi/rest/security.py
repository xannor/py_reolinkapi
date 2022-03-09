""" Security Commands """
from __future__ import annotations
import inspect

import time
from typing import Callable, TypedDict

from . import connection, encrypt

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


class Security:
    """Security mixin"""

    def __init__(self, *args, **kwargs):
        self._logout_callbacks: list[Callable[[], None]] = []
        self.__token = ""
        super().__init__(*args, **kwargs)
        self.__last_pwd_hash = 0
        self.__token_expires: float = 0
        other: any = self
        if isinstance(other, connection.Connection):
            other._disconnect_callbacks.append(self.logout)
            if not hasattr(self, "_execute"):
                self._execute = other._execute
                self._ensure_connection = other._ensure_connection
                self._https = other._https
        if isinstance(other, encrypt.Encrypt):
            self.__can_encrypt = True
            if not hasattr(self, "_encrypted_login"):
                self._encrypted_login = other._encrypted_login

    @property
    def authenticated(self):
        """authentication status"""
        # we use a 1s offest to give time for simple checks to do an operation
        return self.authentication_timeout > 1

    @property
    def _auth_token(self):
        return self.__token

    @property
    def authentication_timeout(self):
        """authnetication token time remaining"""
        return self.__token_expires - time.time()

    @property
    def authentication_id(self):
        """authentication id"""
        return self.__last_pwd_hash

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        # keep hash of username so we can logout on new info provided
        pwd_hash = hash(username)
        if self.__last_pwd_hash != pwd_hash:
            await self.logout()
            self.__last_pwd_hash = pwd_hash

        if not self._ensure_connection():
            return False

        if self.__can_encrypt and not self._https:
            results = await self._encrypted_login(username, password)
        else:
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
        self.__token = value["Token"]["name"]
        self.__token_expires = time.time() + value["Token"]["leaseTime"]

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
        for callback in self._logout_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        self.__token = ""
        self.__token_expires = 0
