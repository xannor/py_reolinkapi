"""LED 3.10"""

from abc import ABC, abstractmethod
from typing import TypeGuard
from ..connection.model import ErrorResponse, Response
from ..connection.part import Connection as ConnectionPart
from ..errors import ReolinkResponseError
from .typing import LightStates, WhiteLedInfo

from . import command


class LED(ConnectionPart, ABC):
    """LED Mixin"""

    @abstractmethod
    def _create_get_ir_lights(self, channel_id: int) -> command.GetIrLightsRequest:
        ...

    @abstractmethod
    def _is_get_ir_lights_response(
        self, response: Response
    ) -> TypeGuard[command.GetIrLightsResponse]:
        ...

    async def get_ir_lights(self, channel: int = 0):
        """Get IR Light State Info"""

        async for response in self._execute(self._create_get_ir_lights(channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get IR Lights failed")

            if self._is_get_ir_lights_response(response):
                return response.state

        raise ReolinkResponseError("Get IR Lights failed")

    @abstractmethod
    def _create_set_ir_lights(
        self, state: LightStates, channel_id: int
    ) -> command.SetIrLightsRequest:
        ...

    async def set_ir_lights(self, state: LightStates, channel: int = 0):
        """Set IR Light State"""

        async for response in self._execute(self._create_set_ir_lights(state, channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set IR Lights failed")

            if self._is_success_response(response):
                return True

        raise ReolinkResponseError("Set IR Lights failed")

    @abstractmethod
    def _create_get_power_led(self, channel_id: int) -> command.GetPowerLedRequest:
        ...

    @abstractmethod
    def _is_get_power_led_response(
        self, response: Response
    ) -> TypeGuard[command.GetPowerLedResponse]:
        ...

    async def get_power_led(self, channel: int = 0):
        """Get Power Led State Info"""

        async for response in self._execute(self._create_get_power_led(channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get Power Led failed")

            if self._is_get_power_led_response(response):
                return response.state

        raise ReolinkResponseError("Get Power Led failed")

    @abstractmethod
    def _create_set_power_led(
        self, state: LightStates, channel_id: int
    ) -> command.SetPowerLedRequest:
        ...

    async def set_power_led(self, state: LightStates, channel: int):
        """Set Power Led State"""

        async for response in self._execute(self._create_set_power_led(state, channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set Power Led failed")

            if self._is_success_response(response):
                return True

        raise ReolinkResponseError("Set Power Led failed")

    @abstractmethod
    def _create_get_white_led(self, channel_id: int) -> command.GetWhiteLedRequest:
        ...

    @abstractmethod
    def _is_get_white_led_response(
        self, response: Response
    ) -> TypeGuard[command.GetWhiteLedResponse]:
        ...

    async def get_white_led(self, channel: int = 0):
        """Get White Led State Info"""

        async for response in self._execute(self._create_get_power_led(channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get White Led failed")

            if self._is_get_white_led_response(response):
                return response.info

        raise ReolinkResponseError("Get White Led failed")

    @abstractmethod
    def _create_set_white_led(
        self,
        info: WhiteLedInfo,
        channel_id: int,
    ) -> command.SetWhiteLedRequest:
        ...

    async def set_white_led(
        self,
        value: WhiteLedInfo,
        channel: int = 0,
    ):
        """Set White Led State"""

        async for response in self._execute(self._create_set_white_led(value, channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set White Led failed")

            if self._is_success_response(response):
                return True

        raise ReolinkResponseError("Set White Led failed")
