"""Commands"""

from abc import ABC
from typing import Any, Protocol, Type, runtime_checkable

from ..errors import ReolinkResponseError

# pylint: disable=too-few-public-methods


class CommandResponse(Protocol):
    """Command Response"""


@runtime_checkable
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


@runtime_checkable
class CommandErrorResponse(CommandResponse, ErrorResponseValue, Protocol):
    """Command Error Response"""

    def throw(self, *args):
        """throw as error"""
        raise ReolinkResponseError(*args, self.error_code, self.details)


class CommandRequest(Protocol):
    """Command Request"""
