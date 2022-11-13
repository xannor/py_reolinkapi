"""Command Models"""

from __future__ import annotations

from abc import ABC
from inspect import isabstract
from typing import Callable

from ..errors import ReolinkResponseError

from .typing import ErrorResponseValue


class Request(ABC):
    """API Request"""

    __slots__ = ()

    id: int


class Response(ABC):
    """API Response"""

    __slots__ = ()

    __handlers: list[ResponseHandler] = []

    request_id: int | None

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if (
            not isabstract(cls)
            and hasattr(cls, "from_response")
            and callable(cls.from_response)
            and cls.from_response is not Response.from_response
        ):
            Response.__handlers.append(cls.from_response)

    @classmethod
    def from_response(cls, response: any, request: Request | None = None) -> "Response" | None:
        """Returns constructed class if response is valid otherwise None"""
        assert cls is Response
        for handler in cls.__handlers:
            if result := handler(response, request):
                return result
        return None


ResponseHandler = Callable[[any, Request | None], Response | None]


class ErrorResponse(Response, ErrorResponseValue, ABC):
    """API Response Error"""

    def throw(self, *args):
        """throw as error"""
        raise ReolinkResponseError(*args, code=self.error_code, details=self.details)
