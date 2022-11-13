"""PTZ 3.7"""

from abc import ABC, abstractmethod
from typing import TypeGuard

from ..connection.model import ErrorResponse, Response
from ..connection.part import Connection as ConnectionPart
from ..errors import ReolinkResponseError
from .typing import Operation, Patrol, Preset, Track, ZoomOperation

from . import command


class PTZ(ConnectionPart, ABC):
    """PTZ commands Mixin"""

    @abstractmethod
    def _create_get_ptz_presets(self, channel_id: int) -> command.GetPresetRequest:
        ...

    @abstractmethod
    def _is_get_ptz_presets_response(
        self, response: Response
    ) -> TypeGuard[command.GetPresetResponse]:
        ...

    async def get_ptz_presets(self, channel: int = 0):
        """Get PTZ Presets"""

        async for response in self._execute(self._create_get_ptz_presets(channel)):
            if not isinstance(response, Response):
                break

            if self._is_get_ptz_presets_response(response):
                return response.presets

            if isinstance(response, ErrorResponse):
                response.throw("Get PTZ Presets failed")

        raise ReolinkResponseError("Get PTZ Presets failed")

    @abstractmethod
    def _create_set_ptz_preset(self, channel_id: int, preset: Preset) -> command.SetPresetRequest:
        ...

    async def set_ptz_preset(self, preset: Preset, channel: int = 0):
        """Set PTZ Preset"""

        async for response in self._execute(self._create_set_ptz_preset(channel, preset)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set PTZ Preset failed")

            if self._is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Preset failed")

    @abstractmethod
    def _create_get_ptz_patrols(self, channel_id: int) -> command.GetPatrolRequest:
        ...

    @abstractmethod
    def _is_get_ptz_patrols_response(
        self, response: Response
    ) -> TypeGuard[command.GetPatrolResponse]:
        ...

    async def get_ptz_patrols(self, channel: int = 0):
        """Get PTZ Patrols"""

        async for response in self._execute(self._create_get_ptz_patrols(channel)):
            if not isinstance(response, Response):
                break

            if self._is_get_ptz_patrols_response(response):
                return response.patrols

            if isinstance(response, ErrorResponse):
                response.throw("Get PTZ Patrols failed")

        raise ReolinkResponseError("Get PTZ Patrols failed")

    @abstractmethod
    def _create_set_ptz_patrol(self, channel_id: int, patrol: Patrol) -> command.SetPatrolRequest:
        ...

    async def set_ptz_patrol(self, patrol: Patrol, channel: int = 0):
        """Set PTZ Patrol"""

        async for response in self._execute(self._create_set_ptz_patrol(channel, patrol)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set PTZ Preset failed")

            if self._is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Preset failed")

    @abstractmethod
    def _create_get_ptz_tatterns(self, channel_id: int) -> command.GetTatternRequest:
        ...

    @abstractmethod
    def _is_get_ptz_tatterns_response(
        self, response: Response
    ) -> TypeGuard[command.GetTatternResponse]:
        ...

    async def get_ptz_tatterns(self, channel: int = 0):
        """Get PTZ Tatterns"""

        async for response in self._execute(self._create_get_ptz_tatterns(channel)):
            if not isinstance(response, Response):
                break

            if self._is_get_ptz_tatterns_response(response):
                return response.tracks

            if isinstance(response, ErrorResponse):
                response.throw("Get PTZ Tatterns failed")

        raise ReolinkResponseError("Get PTZ Tatterns failed")

    @abstractmethod
    def _create_set_ptz_tatterns(self, channel_id: int, *track: Track) -> command.SetTatternRequest:
        ...

    async def set_ptz_tattern(self, *tracks: Track, channel: int = 0):
        """Set PTZ Tattern"""

        async for response in self._execute(self._create_set_ptz_tatterns(channel, *tracks)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set PTZ Tattern failed")

            if self._is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Tattern failed")

    @abstractmethod
    def _create_set_ptz_control(
        self,
        channel_id: int,
        operation: Operation,
        speed: int | None,
        preset_id: int | None,
    ) -> command.SetControlRequest:
        ...

    async def ptz_control(
        self,
        operation: Operation,
        speed: int | None = None,
        preset_id: int | None = None,
        channel: int = 0,
    ):
        ...

        async for response in self._execute(
            self._create_set_ptz_control(channel, operation, speed, preset_id)
        ):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set PTZ Control failed")

            if self._is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Control failed")

    @abstractmethod
    def _create_get_ptz_autofocus(self, channel_id: int) -> command.GetAutoFocusRequest:
        ...

    @abstractmethod
    def _is_get_ptz_autofocus_response(
        self, response: Response
    ) -> TypeGuard[command.GetAutoFocusResponse]:
        ...

    async def get_ptz_autofocus_disabled(self, channel: int = 0):
        """Get PTZ AutoFocus"""

        async for response in self._execute(self._create_get_ptz_autofocus(channel)):
            if not isinstance(response, Response):
                break

            if self._is_get_ptz_autofocus_response(response):
                return not response.disabled

            if isinstance(response, ErrorResponse):
                response.throw("Get PTZ AutoFocus failed")

        raise ReolinkResponseError("Get PTZ AutoFocus failed")

    @abstractmethod
    def _create_set_ptz_autofocus(
        self, channel_id: int, disabled: bool
    ) -> command.SetAutoFocusRequest:
        ...

    async def set_ptz_autofocus(self, disabled: bool, channel: int = 0):
        """Set PTZ AutoFocus"""

        async for response in self._execute(self._create_set_ptz_autofocus(channel, disabled)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set PTZ AutoFocus failed")

            if self._is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ AutoFocus failed")

    @abstractmethod
    def _create_get_ptz_zoom_focus(self, channel_id: int) -> command.GetZoomFocusRequest:
        ...

    @abstractmethod
    def _is_get_ptz_zoom_focus_response(
        self, response: Response
    ) -> TypeGuard[command.GetZoomFocusResponse]:
        ...

    async def get_ptz_zoom_focus(self, channel: int = 0):
        """Get PTZ Zoom and Focus"""

        async for response in self._execute(self._create_get_ptz_zoom_focus(channel)):
            if not isinstance(response, Response):
                break

            if self._is_get_ptz_zoom_focus_response(response):
                return response.state

            if isinstance(response, ErrorResponse):
                response.throw("Get PTZ Zoom Focus failed")

        raise ReolinkResponseError("Get PTZ Zoom Focus failed")

    @abstractmethod
    def _create_set_ptz_zoom_focus(
        self, channel_id: int, operation: ZoomOperation, position: int
    ) -> command.SetZoomFocusRequest:
        ...

    async def set_ptz_zoom_focus(
        self,
        position: int,
        operation: ZoomOperation = ZoomOperation.ZOOM,
        channel: int = 0,
    ):
        """Set PTZ Zoom"""

        async for response in self._execute(
            self._create_set_ptz_zoom_focus(channel, operation, position)
        ):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set PTZ Zoom/Focus failed")

            if self._is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Zoom/Focus failed")
