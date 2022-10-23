"""Alarm Commands"""

from typing import Protocol, TypeGuard

from ..connection.typing import (
    ChannelValue,
    CommandFactory,
    CommandRequest,
    CommandResponse,
)


class GetMotionStateRequest(CommandRequest, ChannelValue, Protocol):
    """Get Motion State Request"""


class GetMotionStateResponse(CommandResponse, ChannelValue, Protocol):
    """Get Mostion State Response"""

    state: bool


class CommandFactory(CommandFactory, Protocol):
    """Alarm Command Factory"""

    def create_get_md_state(self, channel_id: int) -> GetMotionStateRequest:
        """create GetMotionStateRequest"""

    def is_get_md_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetMotionStateResponse]:
        """is GetMotionStateResponse"""
