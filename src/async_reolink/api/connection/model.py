"""Command Models"""

from __future__ import annotations

from abc import ABC
from asyncio import Protocol
from inspect import isabstract

from ..errors import ReolinkResponseError

from .typing import ErrorResponseValue


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
        if objType is self._class:
            return self
        raise AttributeError()

    def __call__(self, response: any, /, request: Request | None = None, **kwds: any):
        for handler in self._handlers:
            if result := handler(response, request, **kwds):
                return result
        return None

    def register(self, handler: ResponseHandler):
        self._handlers.append(handler)


class Response(ABC):
    """API Response"""

    __slots__ = ()

    request_id: int | None

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if (
            not isabstract(cls)
            and (handler := getattr(cls, "from_response", None))
            and callable(handler)
        ):
            Response.from_response.register(handler)

    from_response = ResponseFactory()


class ErrorResponse(Response, ErrorResponseValue, ABC):
    """API Response Error"""

    def throw(self, *args):
        """throw as error"""
        raise ReolinkResponseError(*args, code=self.error_code, details=self.details)
