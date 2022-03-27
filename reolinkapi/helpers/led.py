"""LED Helpers"""

from typing import Final, Iterable, TypedDict

from ..typings.commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)

from ..helpers import commands as commandHelpers

from ..typings.led import AiDetectType, LightState, LightingSchedule, WhiteLedInfo


class GetIrLightsResponseValue(TypedDict):
    """Get IR Lights Response Value"""

    IrLights: LightState


GET_IR_LIGHTS_COMMAND: Final = "GetIrLights"

_isIrLightsCmd = commandHelpers.create_is_command(GET_IR_LIGHTS_COMMAND)

_isIrLights = commandHelpers.create_value_has_key("IrLights", GetIrLightsResponseValue)


def get_ir_lights_responses(responses: Iterable[CommandResponse]):
    """Get IR Light state Responses"""
    return map(
        lambda response: response["value"]["IrLights"],
        filter(
            _isIrLights,
            filter(
                commandHelpers.isvalue,
                filter(_isIrLightsCmd, responses),
            ),
        ),
    )


def create_get_ir_lights(
    channel: int, _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
):
    """Create IR Light state Request"""
    return CommandRequestWithParam(
        cmd=GET_IR_LIGHTS_COMMAND,
        action=_type,
        param=CommandChannelParameter(channel=channel),
    )


class SetIrLightsParameter(TypedDict):
    """Set IR Lights State"""

    IrLights: LightState


SET_IR_LIGHTS_COMMAND: Final = "SetIrLights"


def create_set_ir_lights(
    channel: int,
    state: str,
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create Set IR State Request"""
    return CommandRequestWithParam(
        cmd=SET_IR_LIGHTS_COMMAND,
        action=_type,
        param=SetIrLightsParameter(IrLights=LightState(channel=channel, state=state)),
    )


class GetPowerLedResponseValue(TypedDict, total=False):
    """Get Power Led Response Value"""

    PowerLed: LightState


GET_POWER_LED_COMMAND: Final = "GetPowerLed"

_isPowerLedCmd = commandHelpers.create_is_command(GET_POWER_LED_COMMAND)

_isPowerLed = commandHelpers.create_value_has_key(
    "channel", GetPowerLedResponseValue, int
)


def create_get_power_led(
    channel: int, _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
):
    """Create Power Led state Request"""
    return CommandRequestWithParam(
        cmd=GET_POWER_LED_COMMAND,
        action=_type,
        param=CommandChannelParameter(channel=channel),
    )


def get_power_led_responses(responses: Iterable[CommandResponse]):
    """Get Power Led state Responses"""

    return map(
        lambda response: response["value"]["PowerLed"],
        filter(
            _isPowerLed,
            filter(
                commandHelpers.isvalue,
                filter(_isPowerLedCmd, responses),
            ),
        ),
    )


class SetPowerLedParameter(TypedDict):
    """Set Power Led State"""

    PowerLed: LightState


SET_POWER_LED_COMMAND: Final = "SetPowerLed"


def create_set_power_led(
    state: str,
    channel: int,
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create Power Led State Request"""
    return CommandRequestWithParam(
        cmd=SET_POWER_LED_COMMAND,
        action=_type,
        param=SetPowerLedParameter(PowerLed=LightState(channel=channel, state=state)),
    )


class GetWhiteLedResponseValue(TypedDict, total=False):
    """Get White Led Response Value"""

    WhiteLed: WhiteLedInfo


GET_WHITE_LED_COMMAND: Final = "GetWhiteLed"

_isGetWhileLedCmd = commandHelpers.create_is_command(GET_WHITE_LED_COMMAND)

_isWhiteLed = commandHelpers.create_value_has_key(
    "channel", GetWhiteLedResponseValue, int
)


def create_get_white_led(
    channel: int, _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
):
    """Create White Led state Request"""
    return CommandRequestWithParam(
        cmd=GET_WHITE_LED_COMMAND,
        action=_type,
        param=CommandChannelParameter(channel=channel),
    )


def get_white_led_responses(responses: Iterable[CommandResponse]):
    """Get White Led state Responses"""

    return map(
        lambda response: response["value"]["WhiteLed"],
        filter(
            _isWhiteLed,
            filter(
                commandHelpers.isvalue,
                filter(_isGetWhileLedCmd, responses),
            ),
        ),
    )


def create_set_white_led(
    channel: int,
    state: str,
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    *,
    bright: int = None,
    mode: int = None,
    schedule: LightingSchedule = None,
    ai: AiDetectType = None
):
    """Create White Led State Request"""
    return CommandRequestWithParam(
        cmd=SET_POWER_LED_COMMAND,
        action=_type,
        param=SetWhiteLedParameter(
            WhiteLed=WhiteLedInfo(
                channel=channel,
                state=state,
                bright=bright,
                mode=mode,
                LightingSchedule=schedule,
                wlAiDetectType=ai,
            )
        ),
    )


class SetWhiteLedParameter(TypedDict):
    """Set White Led State"""

    WhiteLed: WhiteLedInfo


SET_WHITE_LED_COMMAND: Final = "SetWhiteLed"
