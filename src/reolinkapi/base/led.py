"""LED Commands"""
from __future__ import annotations

from ..typings.led import AiDetectType, LightingSchedule

from ..helpers import led as ledHelpers, commands as commandHelpers


from . import connection


class LED:
    """LED Mixin"""

    async def get_ir_lights(self, channel: int = 0):
        """Get IR Light State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(ledHelpers.create_get_ir_lights(channel))
        else:
            return None

        value = next(ledHelpers.get_ir_lights_responses(responses), None)
        if value is not None:
            return value["state"]

    async def set_ir_lights(self, state: str, channel: int = 0):
        """Set IR Light State"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                ledHelpers.create_set_ir_lights(channel, state)
            )
        else:
            return False

        return 200 in commandHelpers.get_response_codes(responses)

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(ledHelpers.create_get_power_led(channel))
        else:
            return None

        value = next(ledHelpers.get_power_led_responses(responses), None)
        if value is not None:
            return value["state"]

    async def set_power_led(self, state: str, channel: int):
        """Set Power Led State"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                ledHelpers.create_set_power_led(channel, state)
            )
        else:
            return False

        return 200 in commandHelpers.get_response_codes(responses)

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(ledHelpers.create_get_white_led(channel))
        else:
            return None

        value = next(ledHelpers.get_white_led_responses(responses), None)
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
                ledHelpers.create_set_white_led(
                    channel, state, bright=bright, mode=mode, schedule=schedule, ai=ai
                )
            )
        else:
            return False

        return 200 in commandHelpers.get_response_codes(responses)
