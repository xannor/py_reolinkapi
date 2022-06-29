"""LED 3.10"""

from dataclasses import dataclass
from typing import Final, TypedDict
from typing_extensions import TypeGuard

try:
    from enum import StrEnum  # pylint: disable=ungrouped-imports
except ImportError:
    from backports.strenum import StrEnum

from .commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
)
from . import connection


class LightStates(StrEnum):
    """Light States"""

    AUTO = "Auto"
    ON = "On"
    OFF = "Off"


@dataclass
class LightState:
    """Light State"""

    channel: int
    state: LightStates


class LightStateType(TypedDict, total=False):
    """Light State"""

    state: str


@dataclass
class LightingSchedule:
    """Lighting Schedule"""

    StartHour: int
    StartMin: int
    EndHour: int
    EndMin: int


@dataclass
class AiDetectType:
    """AI Detect Types"""

    dog_cat: int
    face: int
    people: int
    vehicle: int


@dataclass
class WhiteLedInfo:
    """White Led Info"""

    channel: int
    bright: int
    mode: int
    state: int
    LightingSchedule: LightingSchedule
    wlAiDetectType: AiDetectType


class LED:
    """LED Mixin"""

    async def get_ir_lights(self, channel: int = 0):
        """Get IR Light State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetIrLightsRequest(channel))
        else:
            return None

        value = next(filter(GetIrLightsRequest.is_response, responses), None)
        if value is not None:
            return value["IrLights"]["state"]

    async def set_ir_lights(self, state: str, channel: int = 0):
        """Set IR Light State"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                SetIrLightsCommand(channel, state)
            )
        else:
            return False

        return 200 in map(SetIrLightsCommand.get_response_code, responses)

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetPowerLedCommand(channel))
        else:
            return None

        value = next(filter(GetPowerLedCommand.is_response, responses), None)
        if value is not None:
            return value["PowerLed"]["state"]

    async def set_power_led(self, state: str, channel: int):
        """Set Power Led State"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                SetPowerLedCommand(channel, state)
            )
        else:
            return False

        return 200 in map(SetPowerLedCommand.get_response_code, responses)

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetWhiteLedCommand(channel))
        else:
            return None

        value = next(filter(GetWhiteLedCommand.is_response, responses), None)
        if value is not None:
            return value["WhiteLed"]

    async def set_white_led(
        self,
        state: str,
        channel: int,
        *,
        bright: int = None,
        mode: int = None,
        schedule: LightingSchedule = None,
        ai: AiDetectType = None
    ):
        """Set White Led State"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                SetWhiteLedCommand(
                    channel, state, bright=bright, mode=mode, schedule=schedule, ai=ai
                )
            )
        else:
            return False

        return 200 in map(SetWhiteLedCommand.get_response_code, responses)


class GetIrLightsResponseValueType(TypedDict):
    """Get IR Lights Response Value"""

    IrLights: LightStateType


class GetIrLightsRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get IR Lights"""

    COMMAND: Final = "GetIrLights"
    RESPONSE: Final = "IrLights"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetIrLightsResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetIrLightsResponseValueType)
        )


@dataclass
class SetIrLightsParameter:
    """Set IR Lights State"""

    IrLights: LightState


class SetIrLightsCommand(CommandRequestWithParam[SetIrLightsParameter]):
    """Set Ir Lights"""

    COMMAND: Final = "SetIrLights"

    def __init__(self, state: LightStates, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action,
                         SetIrLightsParameter(LightState(channel, state)))


class GetPowerLedResponseValueType(TypedDict, total=False):
    """Get Power Led Response Value"""

    PowerLed: LightStateType


class GetPowerLedCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Power Led"""

    COMMAND: Final = "GetPowerLed"
    RESPONSE: Final = "channel"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetPowerLedResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetPowerLedResponseValueType)
        )


class SetPowerLedParameter:
    """Set Power Led State"""

    PowerLed: LightState


class SetPowerLedCommand(CommandRequestWithParam[SetPowerLedParameter]):
    """Set Ir Lights"""

    COMMAND: Final = "SetPowerLed"

    def __init__(self, state: LightStates, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action,
                         SetPowerLedParameter(LightState(channel, state)))


class GetWhiteLedResponseValueType(TypedDict, total=False):
    """Get White Led Response Value"""

    WhiteLed: WhiteLedInfo


class GetWhiteLedCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Power Led"""

    COMMAND: Final = "GetWhiteLed"
    RESPONSE: Final = "channel"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetWhiteLedResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetWhiteLedResponseValueType)
        )


@dataclass
class SetWhiteLedParameter:
    """Set White Led State"""

    WhiteLed: WhiteLedInfo


class SetWhiteLedCommand(CommandRequestWithParam[SetWhiteLedParameter]):
    """Set Ir Lights"""

    COMMAND: Final = "SetWhiteLed"

    def __init__(
        self,
        state: str,
        channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
        *,
        bright: int = None,
        mode: int = None,
        schedule: LightingSchedule = None,
        ai: AiDetectType = None
    ):
        super().__init__(type(self).COMMAND, action, SetWhiteLedParameter(WhiteLedInfo(
            channel=channel,
            state=state,
            bright=bright,
            mode=mode,
            LightingSchedule=schedule,
            wlAiDetectType=ai,
        )))
