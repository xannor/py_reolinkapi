"""Abstract base connection part"""

from abc import ABC, abstractmethod
from typing import Callable, Iterable

from ..typings.commands import CommandRequest, CommandResponse

from ..const import DEFAULT_TIMEOUT

DISCONNECT_CALLBACK_TYPE = Callable[[], None]


class Connection(ABC):
    """Abstract Connection Mixin"""

    def __init__(self) -> None:
        self._disconnect_callbacks: list[DISCONNECT_CALLBACK_TYPE] = []
        super().__init__()

    @property
    @abstractmethod
    def connection_id(self) -> int:
        """connection id"""
        ...

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
        ...

    @abstractmethod
    def _ensure_connection(self) -> bool:
        ...

    @abstractmethod
    async def disconnect(self):
        """disconnect from device"""
        ...

    @abstractmethod
    async def _execute(self, *args: CommandRequest) -> Iterable[CommandResponse]:
        ...

    async def batch(self, commands: Iterable[CommandRequest]):
        """Execute a batch of commands"""

        return await self._execute(*commands)
