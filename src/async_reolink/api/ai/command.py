"""AI Commands"""

from typing import Mapping, MutableMapping, Protocol, TypeGuard

from ..connection.typing import ChannelValue
from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from .typing import AITypes, AlarmState, Config


class GetAiStateRequest(CommandRequest, ChannelValue, Protocol):
    """Get AI State"""


class GetAiStateResponse(CommandResponse, ChannelValue, Protocol):
    """Get AI State Response"""

    state: Mapping[AITypes, AlarmState]


class GetAiConfigRequest(CommandRequest, ChannelValue, Protocol):
    """Get AI Configuration"""


class GetAiConfigResponse(CommandResponse, ChannelValue, Protocol):
    """Get AI Configuration Response"""

    config: Config


class SetAiConfigRequest(CommandRequest, ChannelValue, Protocol):
    """Set AI Configuration"""

    detect_type: MutableMapping[AITypes, bool]
    ai_track: bool
    track_type: MutableMapping[AITypes, bool]


class CommandFactory(WithCommandFactory, Protocol):
    """AI Command Factory"""

    def create_get_ai_state_request(self, channel_id: int) -> GetAiStateRequest:
        """create GetAiStateRequest"""

    def is_get_ai_state_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetAiStateResponse]:
        """is GetAiStateResponse"""

    def create_get_ai_config_request(self, channel_id: int) -> GetAiConfigRequest:
        """create GetAiConfigRequest"""

    def is_get_ai_config_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetAiConfigResponse]:
        """is GetAiConfigResponse"""

    def create_set_ai_config(
        self, channel_id: int, config: Config
    ) -> SetAiConfigRequest:
        """create SetAiConfigRequest"""
