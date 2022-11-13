"""Connection Parts"""

from typing import AsyncIterable, Callable, Coroutine, Protocol, TypeGuard

from .typing import ResponseCode

from .model import ErrorResponse, Request, Response


class Connection(Protocol):
    """Connection Mixin"""

    _connect_callbacks: list[Callable[[], Coroutine[any, any, None] | None]]
    _disconnect_callbacks: list[Callable[[], Coroutine[any, any, None] | None]]
    _error_handlers: list[Callable[[ErrorResponse], bool | None]]

    hostname: str
    is_connected: bool

    def _has_response_code(self, response: Response) -> TypeGuard[ResponseCode]:
        ...

    def _is_success_response(self, response: Response) -> bool:
        ...

    def _execute(self, *args: Request) -> AsyncIterable[Response | bytes]:
        ...
