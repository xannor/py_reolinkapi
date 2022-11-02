"""Commands"""

from abc import ABC
from typing import (
    AsyncIterable,
    Callable,
    Coroutine,
    Generic,
    Protocol,
    TypeGuard,
    TypeVar,
)

from ..errors import ReolinkResponseError

# pylint: disable=too-few-public-methods


class CommandResponse(Protocol):
    """Command Response"""


class ResponseCode(Protocol):
    """Command Response Code"""

    response_code: int


class ChannelValue(Protocol):
    """Channel Value"""

    channel_id: int


class ErrorResponseValue(Protocol):
    """Error Response Value"""

    error_code: int
    details: str | None


class CommandErrorResponse(CommandResponse, ErrorResponseValue, ABC):
    """Command Error Response"""

    def throw(self, *args):
        """throw as error"""
        raise ReolinkResponseError(*args, code=self.error_code, details=self.details)


class CommandRequest(Protocol):
    """Command Request"""


class CommandFactory(Protocol):
    """Command Factory"""

    def is_request(self, request: any) -> TypeGuard[CommandRequest]:
        """is CommandRequest"""

    def is_response(self, response: any) -> TypeGuard[CommandResponse]:
        """is CommandResponse"""

    def is_error(self, response: CommandResponse) -> TypeGuard[CommandErrorResponse]:
        """is CommandErrorResponse"""

    def is_success(self, response: CommandResponse) -> TypeGuard[ResponseCode]:
        """is successful response"""


_T = TypeVar("_T", bound=CommandFactory)


class WithConnection(Protocol, Generic[_T]):
    """Connection Mixin"""

    _connect_callbacks: list[Callable[[], Coroutine[any, any, None] | None]]
    _disconnect_callbacks: list[Callable[[], Coroutine[any, any, None] | None]]
    _error_handlers: list[Callable[[CommandErrorResponse], bool | None]]

    @property
    def commands(self) -> _T:
        ...

    @property
    def is_connected(self) -> bool:
        ...

    def _execute(self, *args: CommandRequest) -> AsyncIterable[CommandResponse | bytes]:
        ...
