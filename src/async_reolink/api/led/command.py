"""LED Commands"""

from typing import Protocol, TypeGuard

from ..connection.typing import ChannelValue
from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from .typing import LightStates, WhiteLedInfo


class GetIrLightsRequest(CommandRequest, ChannelValue, Protocol):
    """Get IR Lights"""


class GetIrLightsResponse(CommandResponse, ChannelValue, Protocol):
    """Get IR Lights Response"""

    state: LightStates


class SetIrLightsRequest(CommandRequest, ChannelValue, Protocol):
    """Set Ir Lights"""

    state: LightStates


class GetPowerLedRequest(CommandRequest, ChannelValue, Protocol):
    """Get Power Led"""


class GetPowerLedResponse(CommandResponse, ChannelValue, Protocol):
    """Get Power Led Response"""

    state: LightStates


class SetPowerLedRequest(CommandRequest, ChannelValue, Protocol):
    """Set Power Led"""

    state: LightStates


class GetWhiteLedRequest(CommandRequest, ChannelValue, Protocol):
    """Get White Led"""


class GetWhiteLedResponse(CommandResponse, ChannelValue, Protocol):
    """Get White Led Response"""

    info: WhiteLedInfo


class SetWhiteLedRequest(CommandRequest, ChannelValue, Protocol):
    """Set White Led"""

    info: WhiteLedInfo


class CommandFactory(WithCommandFactory, Protocol):
    """LED Command Factory"""

    def create_get_ir_lights_request(self, channel_id: int) -> GetIrLightsRequest:
        """create GetIrLightsRequest"""

    def is_get_ir_lights_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetIrLightsResponse]:
        """is GetIrLightsResponse"""

    def create_set_ir_lights_request(
        self, state: LightStates, channel_id: int
    ) -> SetIrLightsRequest:
        """create SetIrLightsRequest"""

    def create_get_power_led_request(self, channel_id: int) -> GetPowerLedRequest:
        """create GetPowerLedRequest"""

    def is_get_power_led_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetPowerLedResponse]:
        """is GetPowerLedResponse"""

    def create_set_power_led_request(
        self, state: LightStates, channel_id: int
    ) -> SetPowerLedRequest:
        """create SetPowerLedRequest"""

    def create_get_white_led_request(self, channel_id: int) -> GetWhiteLedRequest:
        """create GetWhiteLedRequest"""

    def is_get_white_led_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetWhiteLedResponse]:
        """is GetWhiteLedResponse"""

    def create_set_white_led_request(
        self,
        info: WhiteLedInfo,
        channel_id: int,
    ) -> SetWhiteLedRequest:
        """create SetWhiteLedRequest"""
