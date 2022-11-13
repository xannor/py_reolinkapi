"""Commands"""

from typing import (
    Protocol,
)


# pylint: disable=too-few-public-methods


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
