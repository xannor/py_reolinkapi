"""Command Models"""

from __future__ import annotations

from abc import ABC
from typing import Protocol

from .._utilities.abc import abstractclass, isabstract

from ..errors import ReolinkResponseError

from ..connection.typing import ErrorResponseValue


@abstractclass
class Request(ABC):
    """API Request"""

    __slots__ = ()

    id: int


class ResponseHandler(Protocol):
    """Response Handler Callback"""

    def __call__(
        self, response: any, /, request: Request | None = None, **kwds: any
    ) -> Response | None:
        ...


class ResponseFactory(ResponseHandler):
    """Factory descriptor for handling response creation"""

    __slots__ = ("_handlers", "_class", "_name")

    def __init__(self) -> None:
        self._handlers: list[ResponseHandler] = []

    def __set_name__(self, owner: type, name: str):
        self._name = name
        self._class = owner

    def __get__(self, obj: any, objType: type | None = None):
        if issubclass(objType, self._class):
            return self
        raise AttributeError()

    def __call__(self, response: any, /, request: Request | None = None, **kwds: any):
        for handler in self._handlers:
            if result := handler(response, request=request, **kwds):
                return result
        return None

    def register(self, handler: ResponseHandler):
        self._handlers.append(handler)


@abstractclass
class Response(ABC):
    """API Response"""

    __slots__ = ()

    request_id: int | None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if (
            not isabstract(cls)
            and (handler := getattr(cls, "from_response", None))
            and handler != Response.from_response
            and callable(handler)
        ):
            Response.from_response.register(handler)

    from_response = ResponseFactory()


@abstractclass
class ErrorResponse(Response, ErrorResponseValue, ABC):
    """API Response Error"""

    def throw(__response: ErrorResponseValue, *args):
        """throw as error"""
        raise ReolinkResponseError(*args, code=__response.error_code, details=__response.details)
