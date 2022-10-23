"""Connection"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AsyncIterable, Iterable

from async_reolink.api.connection.typing import CommandRequest, CommandResponse

from ..const import DEFAULT_TIMEOUT

from ..command_factory import CommandFactory

from .typing import WithConnection


class Connection(WithConnection[CommandFactory], ABC):
    """Abstract Connection Mixin"""

    def __init__(self, *args, **kwargs) -> None:
        self._connect_callbacks = []
        self._disconnect_callbacks = []
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
    ):
        """setup connection to device"""

    @abstractmethod
    async def disconnect(self):
        """disconnect from device"""

    @property
    @abstractmethod
    def commands(self) -> CommandFactory.CommandFactory:
        """command factory instance"""

    @abstractmethod
    def _execute(self, *args: CommandRequest) -> AsyncIterable[CommandResponse | bytes]:
        ...

    def batch(
        self,
        commands: Iterable[CommandRequest],
    ):
        """Execute a batch of commands"""

        return self._execute(*commands)
