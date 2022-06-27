"""LED 3.10"""

from dataclasses import dataclass
from enum import Enum
from typing import Final, TypedDict

from pyparsing import Iterable
from .commands import COMMAND, COMMAND_RESPONSE_VALUE, CommandChannelParameter, CommandRequestTypes, CommandRequestWithParam, CommandResponse, create_is_command, create_value_has_key, get_response_codes, isvalue
from . import connection

class LightStates(str, Enum):
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

        value = next(GetIrLightsRequest.get_responses(responses), None)
        if value is not None:
            return value["state"]

    async def set_ir_lights(self, state: str, channel: int = 0):
        """Set IR Light State"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                SetIrLightsRequest(channel, state)
            )
        else:
            return False

        return 200 in get_response_codes(responses)

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetPowerLedRequest(channel))
        else:
            return None

        value = next(GetPowerLedRequest.get_responses(responses), None)
        if value is not None:
            return value["state"]

    async def set_power_led(self, state: str, channel: int):
        """Set Power Led State"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                SetPowerLedRequest(channel, state)
            )
        else:
            return False

        return 200 in get_response_codes(responses)

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetWhiteLedRequest(channel))
        else:
            return None

        value = next(GetWhiteLedRequest.get_responses(responses), None)
        if value is not None:
            return value["state"]

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
                SetWhiteLedParameter(
                    channel, state, bright=bright, mode=mode, schedule=schedule, ai=ai
                )
            )
        else:
            return False

        return 200 in get_response_codes(responses)

class GetIrLightsResponseValue(TypedDict):
    """Get IR Lights Response Value"""

    IrLights: LightStateType

class GetIrLightsRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get IR Lights"""

    COMMAND: Final = "GetIrLights"
    RESPONSE: Final = "IrLights"

    def __init__(self, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """Get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isIrLights,
                filter(
                    isvalue,
                    filter(_isIrLightsCmd, responses),
                ),
            ),
        )

_isIrLightsCmd = create_is_command(GetIrLightsRequest.COMMAND)

_isIrLights = create_value_has_key(GetIrLightsRequest.RESPONSE, GetIrLightsResponseValue)

@dataclass
class SetIrLightsParameter:
    """Set IR Lights State"""

    IrLights: LightState

class SetIrLightsRequest(CommandRequestWithParam[SetIrLightsParameter]):
    """Set Ir Lights"""

    COMMAND: Final = "SetIrLights"

    def __init__(self, state:LightStates, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, SetIrLightsParameter(LightState(channel, state)))


class GetPowerLedResponseValue(TypedDict, total=False):
    """Get Power Led Response Value"""

    PowerLed: LightStateType

class GetPowerLedRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get Power Led"""

    COMMAND: Final = "GetPowerLed"
    RESPONSE: Final = "channel"

    def __init__(self, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """Get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isPowerLed,
                filter(
                    isvalue,
                    filter(_isPowerLedCmd, responses),
                ),
            ),
        )

_isPowerLedCmd = create_is_command(GetPowerLedRequest.COMMAND)

_isPowerLed = create_value_has_key(
    GetPowerLedRequest.RESPONSE, GetPowerLedResponseValue, int
)

class SetPowerLedParameter:
    """Set Power Led State"""

    PowerLed: LightState

class SetPowerLedRequest(CommandRequestWithParam[SetPowerLedParameter]):
    """Set Ir Lights"""

    COMMAND: Final = "SetPowerLed"

    def __init__(self, state:LightStates, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, SetPowerLedParameter(LightState(channel, state)))


class GetWhiteLedResponseValue(TypedDict, total=False):
    """Get White Led Response Value"""

    WhiteLed: WhiteLedInfo

class GetWhiteLedRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get Power Led"""

    COMMAND: Final = "GetWhiteLed"
    RESPONSE: Final = "channel"

    def __init__(self, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """Get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isWhiteLed,
                filter(
                    isvalue,
                    filter(_isGetWhileLedCmd, responses),
                ),
            ),
        )


GET_WHITE_LED_COMMAND: Final = "GetWhiteLed"

_isGetWhileLedCmd = create_is_command(GetWhiteLedRequest.COMMAND)

_isWhiteLed = create_value_has_key(
    GetWhiteLedRequest.RESPONSE, GetWhiteLedResponseValue, int
)

class SetWhiteLedParameter:
    """Set White Led State"""

    WhiteLed: WhiteLedInfo

class SettWhiteLedRequest(CommandRequestWithParam[SetWhiteLedParameter]):
    """Set Ir Lights"""

    COMMAND: Final = "SetWhiteLed"

    def __init__(
        self, 
        state: str,
        channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY,
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



