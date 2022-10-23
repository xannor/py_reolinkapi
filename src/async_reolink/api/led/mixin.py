"""LED 3.10"""

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from ..typing import PercentValue
from .command import CommandFactory
from .typing import LightStates, WhiteLedInfo


class LED(WithConnection[CommandFactory]):
    """LED Mixin"""

    async def get_ir_lights(self, channel: int = 0):
        """Get IR Light State Info"""

        async for response in self._execute(
            self.commands.create_get_ir_lights_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get IR Lights failed")

            if (
                self.commands.is_get_ir_lights_response(response)
                and response.channel_id == channel
            ):
                return response.state

        raise ReolinkResponseError("Get IR Lights failed")

    async def set_ir_lights(self, state: LightStates, channel: int = 0):
        """Set IR Light State"""

        async for response in self._execute(
            self.commands.create_set_ir_lights_request(state, channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set IR Lights failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set IR Lights failed")

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        async for response in self._execute(
            self.commands.create_get_power_led_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get Power Led failed")

            if (
                self.commands.is_get_power_led_response(response)
                and response.channel_id == channel
            ):
                return response.state

        raise ReolinkResponseError("Get Power Led failed")

    async def set_power_led(self, state: LightStates, channel: int):
        """Set Power Led State"""

        async for response in self._execute(
            self.commands.create_set_power_led_request(state, channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set Power Led failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set Power Led failed")

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        async for response in self._execute(
            self.commands.create_get_power_led_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get White Led failed")

            if (
                self.commands.is_get_white_led_response(response)
                and response.channel_id == channel
            ):
                return response.info

        raise ReolinkResponseError("Get White Led failed")

    async def set_white_led(
        self,
        value: WhiteLedInfo,
        channel: int = 0,
    ):
        """Set White Led State"""

        async for response in self._execute(
            self.commands.create_set_white_led_request(value, channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set White Led failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set White Led failed")
