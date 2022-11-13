"""Alarm Commands"""

from typing import Protocol

from ..connection.typing import (
    ChannelValue,
)


class GetMotionStateRequest(ChannelValue, Protocol):
    """Get Motion State Request"""


class GetMotionStateResponse(ChannelValue, Protocol):
    """Get Mostion State Response"""

    state: bool
