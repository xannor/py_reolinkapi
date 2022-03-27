""" Security Commands """
from __future__ import annotations

from ..exceptions import InvalidCredentialsError

from reolinkapi.typings.commands import CommandResponse

from . import encrypt

from ..const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from ..base.security import Security as BaseSecurity
from ..helpers import security as securityHelpers

from . import connection


class Security(BaseSecurity):
    """Security mixin"""

    def __init__(self) -> None:
        super().__init__()
        if isinstance(self, connection.Connection):
            self._process_responses_callbacks.append(self.__process_responses)

    def __process_responses(self, responses: list[CommandResponse]):
        if securityHelpers.has_auth_failure(responses):
            raise InvalidCredentialsError()

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ) -> bool:
        """attempt to log into device"""

        if not await self._prelogin(username):
            return False

        if isinstance(self, encrypt.Encrypt):
            if self._can_encrypt:
                results = await self._encrypted_login(username, password)
                if results is not None:
                    return self._process_token(results)

        return self._process_token(await self._do_login(username, password))
