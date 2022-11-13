"""Securty Parts"""

from typing import Callable, Protocol
from .typing import AuthenticationId


class Security(Protocol):
    """Security Part"""

    _logout_callbacks: list[Callable[[], None]]

    authentication_id: AuthenticationId

    def _create_authentication_id(
        self, username: str, password: str | None = None
    ) -> AuthenticationId:
        ...
