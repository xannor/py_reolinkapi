"""Connection"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AsyncIterable, Callable, Coroutine, Iterable
from .typing import StreamReader

from .const import DEFAULT_TIMEOUT

from .commands import CommandRequest, CommandResponseType

from .errors import ErrorCodes, ReolinkResponseError


def _raise_response_error(code: ErrorCodes, details: str | None = None) -> bool:
    raise ReolinkResponseError(code=code, details=details)


class Connection(ABC):
    """Abstract Connection Mixin"""

    def __init__(self) -> None:
        self._connect_callbacks: list[
            Callable[[], Coroutine[any, any, None] | None]
        ] = []
        self._disconnect_callbacks: list[
            Callable[[], Coroutine[any, any, None] | None]
        ] = []
        super().__init__()

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

    @abstractmethod
    async def _execute(
        self, *args: CommandRequest
    ) -> AsyncIterable[CommandResponseType] | StreamReader:
        ...

    def batch(
        self,
        commands: Iterable[CommandRequest],
        *,
        __trap: Callable[[ErrorCodes, str | None],
                         bool] = _raise_response_error,
    ):
        """Execute a batch of commands"""

        async def _iterate():
            async for response in async_trap_errors(
                await self._execute(*commands), __trap=__trap
            ):
                yield response

        return _iterate()


def async_trap_errors(
    responses: AsyncIterable[CommandResponseType] | StreamReader,
    *,
    __trap: Callable[[ErrorCodes, str | None], bool] = _raise_response_error,
):
    """Trap Response Errors"""
    if isinstance(responses, StreamReader):
        code = ErrorCodes.PROTOCOL_ERROR
        details = "Expected CommandResponses got Stream"
        if not __trap(code, details):
            _raise_response_error(code, details)

        async def _empty_response():
            if TYPE_CHECKING:
                yield CommandResponseType()

        return _empty_response()

    async def _iterate():
        async for response in responses:
            if CommandRequest.is_error(response):
                error = CommandRequest.get_error(response)
                code = ErrorCodes(error["rspCode"])
                if not __trap(code, error.get("detail", None)):
                    _raise_response_error(code, error.get("detail", None))
                continue
            yield response

    return _iterate()
