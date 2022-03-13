"""LED Commands"""
from __future__ import annotations
from typing import Final, Iterable, TypedDict


from ..typings.commands import (
    CommandChannelParameter,
    CommandRequestWithParam,
    CommandRequestTypes,
    CommandResponse,
)

from ..helpers import commands as commandHelpers

from . import connection
from ..typings.led import AiDetectType, LightState, LightingSchedule, WhiteLedInfo


class GetIrLightsResponseValue(TypedDict):
    """Get IR Lights Response Value"""

    IrLights: LightState


GET_IR_LIGHTS_COMMAND: Final = "GetIrLights"

_isIrLights = commandHelpers.create_value_has_key("IrLights", GetIrLightsResponseValue)


def _get_ir_lights_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"]["IrLights"],
        filter(
            _isIrLights,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_IR_LIGHTS_COMMAND, responses
                ),
            ),
        ),
    )


class SetIrLightsParameter(TypedDict):
    """Set IR Lights State"""

    IrLights: LightState


SET_IR_LIGHTS_COMMAND: Final = "SetIrLights"


class GetPowerLedResponseValue(TypedDict, total=False):
    """Get Power Led Response Value"""

    PowerLed: LightState


GET_POWER_LED_COMMAND: Final = "GetPowerLed"

_isPowerLed = commandHelpers.create_value_has_key(
    "channel", GetPowerLedResponseValue, int
)


def _get_power_led_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"]["PowerLed"],
        filter(
            _isPowerLed,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_POWER_LED_COMMAND, responses
                ),
            ),
        ),
    )


class SetPowerLedParameter(TypedDict):
    """Set Power Led State"""

    PowerLed: LightState


SET_POWER_LED_COMMAND: Final = "SetPowerLed"


class GetWhiteLedResponseValue(TypedDict, total=False):
    """Get White Led Response Value"""

    WhiteLed: WhiteLedInfo


GET_WHITE_LED_COMMAND: Final = "GetWhiteLed"

_isWhiteLed = commandHelpers.create_value_has_key(
    "channel", GetWhiteLedResponseValue, int
)


def _get_white_led_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"]["WhiteLed"],
        filter(
            _isWhiteLed,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_WHITE_LED_COMMAND, responses
                ),
            ),
        ),
    )


class SetWhiteLedParameter(TypedDict):
    """Set White Led State"""

    WhiteLed: WhiteLedInfo


SET_WHITE_LED_COMMAND: Final = "SetWhiteLed"


class LED:
    """LED Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        other: any = self
        if isinstance(other, connection.Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = other._execute

    @staticmethod
    def create_get_ir_lights(
        channel: int, _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ):
        """Create IR Light state Request"""
        return CommandRequestWithParam(
            cmd=GET_IR_LIGHTS_COMMAND,
            action=_type,
            param=CommandChannelParameter(channel=channel),
        )

    @staticmethod
    def get_ir_lights_responses(responses: Iterable[CommandResponse]):
        """Get IR Light state Responses"""

        return _get_ir_lights_responses(responses)

    async def get_ir_lights(self, channel: int = 0):
        """Get IR Light State Info"""

        value = next(
            _get_ir_lights_responses(
                await self._execute(LED.create_get_ir_lights(channel))
            ),
            None,
        )
        if value is not None:
            return value["state"]
        return value

    @staticmethod
    def create_set_ir_lights(
        state: str,
        channel: int,
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create Set IR State Request"""
        return CommandRequestWithParam(
            cmd=SET_IR_LIGHTS_COMMAND,
            action=_type,
            param=SetIrLightsParameter(
                IrLights=LightState(channel=channel, state=state)
            ),
        )

    async def set_ir_lights(self, state: str, channel: int):
        """Set IR Light State"""

        value = next(
            map(
                lambda response: response["value"],
                filter(
                    commandHelpers.isresponse,
                    filter(
                        commandHelpers.isvalue,
                        await self._execute(LED.create_set_ir_lights(state, channel)),
                    ),
                ),
            ),
            None,
        )
        return value is not None and value["rspCode"] == 200

    @staticmethod
    def create_get_power_led(
        channel: int, _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ):
        """Create Power Led state Request"""
        return CommandRequestWithParam(
            cmd=GET_POWER_LED_COMMAND,
            action=_type,
            param=CommandChannelParameter(channel=channel),
        )

    @staticmethod
    def get_power_led_responses(responses: Iterable[CommandResponse]):
        """Get Power Led state Responses"""

        return _get_power_led_responses(responses)

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        value = next(
            _get_power_led_responses(
                await self._execute(LED.create_get_power_led(channel))
            ),
            None,
        )
        if value is not None:
            return value["state"]
        return value

    @staticmethod
    def create_set_power_led(
        state: str,
        channel: int,
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create Power Led State Request"""
        return CommandRequestWithParam(
            cmd=SET_POWER_LED_COMMAND,
            action=_type,
            param=SetPowerLedParameter(
                PowerLed=LightState(channel=channel, state=state)
            ),
        )

    async def set_power_led(self, state: str, channel: int):
        """Set Power Led State"""

        value = next(
            map(
                lambda response: response["value"],
                filter(
                    commandHelpers.isresponse,
                    filter(
                        commandHelpers.isvalue,
                        await self._execute(LED.create_set_power_led(state, channel)),
                    ),
                ),
            ),
            None,
        )
        return value is not None and value["rspCode"] == 200

    @staticmethod
    def create_get_white_led(
        channel: int, _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ):
        """Create White Led state Request"""
        return CommandRequestWithParam(
            cmd=GET_WHITE_LED_COMMAND,
            action=_type,
            param=CommandChannelParameter(channel=channel),
        )

    @staticmethod
    def get_white_led_responses(responses: Iterable[CommandResponse]):
        """Get White Led state Responses"""

        return _get_white_led_responses(responses)

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        value = next(
            _get_white_led_responses(
                await self._execute(LED.create_get_white_led(channel))
            ),
            None,
        )
        if value is not None:
            return value["state"]
        return value

    @staticmethod
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

        value = next(
            map(
                lambda response: response["value"],
                filter(
                    commandHelpers.isresponse,
                    filter(
                        commandHelpers.isvalue,
                        await self._execute(
                            LED.create_set_white_led(
                                state,
                                channel,
                                bright=bright,
                                mode=mode,
                                schedule=schedule,
                                ai=ai,
                            )
                        ),
                    ),
                ),
            ),
            None,
        )
        return value is not None and value["rspCode"] == 200
