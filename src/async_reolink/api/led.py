"""LED 3.10"""

from dataclasses import dataclass
from typing import Final, Literal, TypedDict
from typing_extensions import TypeGuard

from backports.strenum import StrEnum

from .typing import ClockHour, ClockMinutes, IntPercent, OnOffState

from .utils import afilter, alist, amap

from .commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponseValue,
    async_trap_errors,
)
from . import connection


class LightStates(StrEnum):
    """Light States"""

    AUTO = "Auto"
    ON = "On"
    OFF = "Off"


LightStatesValues = Literal["Auto", "On", "Off"]


@dataclass
class LightState:
    """Light State"""

    channel: int
    state: LightStates


class LightStateType(TypedDict, total=False):
    """Light State"""

    state: LightStatesValues


@dataclass
class LightingSchedule:
    """Lighting Schedule"""

    StartHour: ClockHour
    StartMin: ClockMinutes
    EndHour: ClockHour
    EndMin: ClockMinutes


class LightingScheduleType(TypedDict):
    """Lighting Schedule"""

    StartHour: ClockHour
    StartMin: ClockMinutes
    EndHour: ClockHour
    EndMinutes: ClockMinutes


@dataclass
class AiDetect:
    """ AI Detection Trigger"""

    dog_cat: OnOffState
    face: OnOffState
    people: OnOffState
    vehicle: OnOffState


class AiDetectType(TypedDict, total=False):
    """AI Detection Trigger"""

    dog_cat: OnOffState
    face: OnOffState
    people: OnOffState
    vehicle: OnOffState


class WhiteLedInfoType(TypedDict, total=False):
    """White Led Info"""

    channel: int
    bright: IntPercent
    auto: int
    """auto mode - according to API no example given"""
    mode: int
    """brightness state - according to API 0 given as example"""
    state: int
    """state - accoring to API 0 given as example"""
    LightingSchedule: LightingScheduleType
    wlAiDetectType: AiDetectType


class LED:
    """LED Mixin"""

    async def get_ir_lights(self, channel: int = 0):
        """Get IR Light State Info"""

        Command = GetIrLightsRequest

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(channel)
            ))
        else:
            return None

        result = await anext(
            amap(
                Command.get_value,
                afilter(
                    Command.is_response,
                    responses
                )
            ),
            None,
        )

        if result:
            return LightStates(result["state"])
        return None

    async def set_ir_lights(self, state: LightStates, channel: int = 0):
        """Set IR Light State"""

        Command = SetIrLightsCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(state, channel)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        Command = GetPowerLedCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(channel)
            ))
        else:
            return None

        result = await anext(
            amap(
                Command.get_value,
                afilter(
                    Command.is_response,
                    responses
                )
            ),
            None,
        )

        if result:
            return LightStates(result["state"])
        return None

    async def set_power_led(self, state: LightStates, channel: int):
        """Set Power Led State"""

        Command = SetPowerLedCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(state, channel)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        Command = GetWhiteLedCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(channel)
            ))
        else:
            return None

        result = await anext(
            amap(
                Command.get_value,
                afilter(
                    Command.is_response,
                    responses
                )
            ),
            None,
        )

        if result:
            return LightStates(result["state"])
        return None

    async def set_white_led(
        self,
        state: int,
        channel: int,
        *,
        bright: IntPercent = None,
        mode: int = None,
        schedule: LightingSchedule = None,
        ai: AiDetect = None
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
    def is_response(cls, value: any) -> TypeGuard[CommandResponseValue[GetIrLightsResponseValueType]]:  # pylint: disable=arguments-differ
        """Is response"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetIrLightsResponseValueType)
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetIrLightsResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


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
    RESPONSE: Final = "PowerLed"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[CommandResponseValue[GetPowerLedResponseValueType]]:  # pylint: disable=arguments-differ
        """Is response"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetPowerLedResponseValueType)
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetPowerLedResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


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

    WhiteLed: WhiteLedInfoType


class GetWhiteLedCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Power Led"""

    COMMAND: Final = "GetWhiteLed"
    RESPONSE: Final = "WhiteLed"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[CommandResponseValue[GetWhiteLedResponseValueType]]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetWhiteLedResponseValueType)
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetWhiteLedResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


@dataclass
class SetWhiteLedParameter:
    """Set White Led State"""

    WhiteLed: WhiteLedInfoType


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
        super().__init__(type(self).COMMAND, action, SetWhiteLedParameter(WhiteLedInfoType(
            channel=channel,
            state=state,
            bright=bright,
            mode=mode,
            LightingSchedule=schedule,
            wlAiDetectType=ai,
        )))
