"""Abstract base authentication part"""

from abc import ABC
import inspect
from time import time
from typing import Callable, Iterable

from reolinkapi.typings.commands import CommandResponse

from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from ..helpers import security as securityHelpers, commands as commandHelpers

from .connection import Connection

LOGOUT_CALLBACK_TYPE = Callable[[], None]


class Security(ABC):
    """Abstract Security Mixin"""

    def __init__(self) -> None:
        self._logout_callbacks: list[LOGOUT_CALLBACK_TYPE] = []
        self.__token = ""
        super().__init__()
        if isinstance(self, Connection):
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

        if isinstance(self, Connection):
            if not self._ensure_connection():
                return False
        return True

    async def _do_login(self, username: str, password: str):
        if isinstance(self, Connection):
            return await self._execute(securityHelpers.create_login(username, password))
        return []

    def _process_token(self, responses: Iterable[CommandResponse]):
        token = next(securityHelpers.login_responses(responses), None)
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
            if isinstance(self, Connection):
                if self._ensure_connection():
                    errors = list(
                        filter(
                            commandHelpers.iserror,
                            await self._execute(securityHelpers.create_logout()),
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
