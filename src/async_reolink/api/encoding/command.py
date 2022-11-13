"""Encoding Commands"""

from typing import Protocol

from ..connection.typing import ChannelValue
from .typing import EncodingInfo


class GetEncodingRequest(ChannelValue, Protocol):
    """Get Encoding"""


class GetEncodingResponse(ChannelValue, Protocol):
    """Get Encoding Response"""

    info: EncodingInfo
