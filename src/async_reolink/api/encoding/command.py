"""Encoding Commands"""

from typing import Protocol, TypeGuard

from ..connection.typing import ChannelValue
from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from .typing import EncodingInfo


class GetEncodingRequest(CommandRequest, ChannelValue, Protocol):
    """Get Encoding"""


class GetEncodingResponse(CommandResponse, ChannelValue, Protocol):
    """Get Encoding Response"""

    info: EncodingInfo


class CommandFactory(WithCommandFactory, Protocol):
    """Encoding Command Factory"""

    def create_get_encoding_request(self, channel_id: int) -> GetEncodingRequest:
        """create GetEncodingRequest"""

    def is_get_encoding_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetEncodingResponse]:
        """is GetEncodingResponse"""
