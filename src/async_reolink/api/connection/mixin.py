"""Connection"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AsyncIterable, Iterable, TypeGuard

from ..const import DEFAULT_TIMEOUT

from .typing import ResponseCode

from .model import Request, Response

from .part import Connection as ConnectionPart


class Connection(ConnectionPart, ABC):
    """Abstract Connection Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        self._connect_callbacks = []
        self._disconnect_callbacks = []
        self._error_handlers = []
        super().__init__(*args, **kwargs)

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """is connected"""

    @property
    @abstractmethod
    def connection_id(self) -> int:
        """connection id"""

    @property
    @abstractmethod
    def hostname(self):
        """hostname"""

    @property
    def secured(self) -> bool:
        """Secure connection"""
        return False

    @abstractmethod
    async def connect(
        self,
        hostname: str,
        port: int = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> bool:
        """setup connection to device"""

    @abstractmethod
    async def disconnect(self):
        """disconnect from device"""

    @abstractmethod
    def _execute(self, *args: Request) -> AsyncIterable[Response | bytes]:
        ...

    @abstractmethod
    def _has_response_code(self, response: Response) -> TypeGuard[ResponseCode]:
        ...

    @abstractmethod
    def _is_success_response(self, response: Response) -> bool:
        ...

    def batch(
        self,
        commands: Iterable[Request],
    ):
        """Execute a batch of commands"""

        return self._execute(*commands)
