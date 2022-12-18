"""Security"""

import inspect
from abc import ABC, abstractmethod
from typing import TypeGuard

from ..connection.model import ErrorResponse, Response

from ..connection.part import Connection as ConnectionPart
from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME
from ..errors import ReolinkResponseError, ErrorCodes
from .typing import AuthenticationId
from .part import Security as SecurityPart

from . import command


class Security(ConnectionPart, SecurityPart, ABC):
    """Abstract Security Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        self._logout_callbacks = []
        super().__init__(*args, **kwargs)
        self._disconnect_callbacks.append(self.logout)
        self._error_handlers.append(self._intercept_auth_required)

    @property
    @abstractmethod
    def is_authenticated(self) -> bool:
        """authentication status"""

    @property
    @abstractmethod
    def authentication_timeout(self) -> float:
        """authentication time remaining"""

    @property
    @abstractmethod
    def authentication_id(self) -> AuthenticationId:
        """authentication id"""

    @abstractmethod
    def _create_authentication_id(
        self, username: str, password: str | None = None
    ) -> AuthenticationId:
        ...

    async def _prelogin(self, username: str):
        id = self._create_authentication_id(username)
        if self.authentication_id.weak != id.weak:
            await self.logout()

        if not self.is_connected:
            return False
        return True

    @abstractmethod
    async def _process_login(self, response: command.LoginResponse) -> bool:
        ...

    @abstractmethod
    def _create_login(self, username: str, password: str) -> command.LoginRequest:
        ...

    @abstractmethod
    def _is_login_response(
        self, response: Response
    ) -> TypeGuard[command.LoginResponse]:
        ...

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        async for response in self._execute(self._create_login(username, password)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Login request failed")

            if self._is_login_response(response):
                return await self._process_login(response)

        raise ReolinkResponseError("Login request failed")

    @abstractmethod
    def _clear_login(self) -> None:
        ...

    def _intercept_auth_required(self, response: ErrorResponse):
        if response.error_code == ErrorCodes.AUTH_REQUIRED:
            self._clear_login()

    async def _logout(self):
        try:
            for callback in self._logout_callbacks:
                if inspect.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
        finally:
            # whether clean or not logout always succeeds
            self._clear_login()

    @abstractmethod
    def _create_logout(self) -> command.LogoutRequest:
        ...

    async def logout(self) -> None:
        """Clear authentication information"""

        if not self.is_authenticated:
            return

        try:
            async for response in self._execute(self._create_logout()):
                if not isinstance(response, Response):
                    break

                if isinstance(response, ErrorResponse):
                    response.throw("Logout request failed")

                if self._is_success_response(response):
                    return

            raise ReolinkResponseError("Logout request failed")
        finally:
            await self._logout()

    @abstractmethod
    def _create_get_user(self) -> command.GetUserRequest:
        ...

    @abstractmethod
    def _is_get_user_response(
        self, response: Response
    ) -> TypeGuard[command.GetUserResponse]:
        ...

    async def get_users(self):
        """Get Device Users"""

        async for response in self._execute(self._create_get_user()):
            if not isinstance(response, Response):
                break

            if self._is_get_user_response(response):
                return response.users

            if isinstance(response, ErrorResponse):
                response.throw("Get Users request failed")

        raise ReolinkResponseError("Get Users request failed")
