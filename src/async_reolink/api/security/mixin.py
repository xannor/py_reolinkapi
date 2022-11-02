"""Security"""

import inspect
from abc import ABC, abstractmethod

from ..connection.typing import WithConnection, CommandErrorResponse
from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME
from ..errors import ReolinkResponseError, ErrorCodes
from .command import CommandFactory, LoginResponse
from .typing import WithSecurity


class Security(WithConnection[CommandFactory], WithSecurity, ABC):
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
    def authentication_id(self) -> int:
        """authentication id"""

    @abstractmethod
    async def _prelogin(self, username: str) -> bool:
        ...

    @abstractmethod
    async def _process_login(self, response: LoginResponse) -> bool:
        ...

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        async for response in self._execute(self.commands.create_login_request(username, password)):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Login request failed")

            if self.commands.is_login_response(response):
                return await self._process_login(response)

        raise ReolinkResponseError("Login request failed")

    @abstractmethod
    def _clear_login(self) -> None:
        ...

    def _intercept_auth_required(self, response: CommandErrorResponse):
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

    async def logout(self) -> None:
        """Clear authentication information"""

        if not self.is_authenticated:
            return

        try:
            async for response in self._execute(self.commands.create_logout_request()):
                if not self.commands.is_response(response):
                    break

                if self.commands.is_error(response):
                    response.throw("Logout request failed")

                if self.commands.is_success(response):
                    return

            raise ReolinkResponseError("Logout request failed")
        finally:
            await self._logout()

    async def get_users(self):
        """Get Device Users"""

        async for response in self._execute(self.commands.create_get_user_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_user_response(response):
                return response.users

            if self.commands.is_error(response):
                response.throw("Get Users request failed")

        raise ReolinkResponseError("Get Users request failed")
