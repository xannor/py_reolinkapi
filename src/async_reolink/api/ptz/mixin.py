"""PTZ 3.7"""

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from .command import CommandFactory
from .typing import Operation, Patrol, Preset, Track, ZoomOperation


class PTZ(WithConnection[CommandFactory]):
    """PTZ commands Mixin"""

    async def get_ptz_presets(self, channel: int = 0):
        """Get PTZ Presets"""

        async for response in self._execute(self.commands.create_get_ptz_presets_request(channel)):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_ptz_presets_response(response):
                return response.presets

            if self.commands.is_error(response):
                response.throw("Get PTZ Presets failed")

        raise ReolinkResponseError("Get PTZ Presets failed")

    async def set_ptz_preset(self, preset: Preset, channel: int = 0):
        """Set PTZ Preset"""

        async for response in self._execute(
            self.commands.create_set_ptz_preset_request(channel, preset)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set PTZ Preset failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Preset failed")

    async def get_ptz_patrols(self, channel: int = 0):
        """Get PTZ Patrols"""

        async for response in self._execute(self.commands.create_get_ptz_patrols_request(channel)):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_ptz_patrols_response(response):
                return response.patrols

            if self.commands.is_error(response):
                response.throw("Get PTZ Patrols failed")

        raise ReolinkResponseError("Get PTZ Patrols failed")

    async def set_ptz_patrol(self, patrol: Patrol, channel: int = 0):
        """Set PTZ Patrol"""

        async for response in self._execute(
            self.commands.create_set_ptz_patrol_request(channel, patrol)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set PTZ Preset failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Preset failed")

    async def get_ptz_tatterns(self, channel: int = 0):
        """Get PTZ Tatterns"""

        async for response in self._execute(self.commands.create_get_ptz_tatterns_request(channel)):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_ptz_tatterns_response(response):
                return response.tracks

            if self.commands.is_error(response):
                response.throw("Get PTZ Tatterns failed")

        raise ReolinkResponseError("Get PTZ Tatterns failed")

    async def set_ptz_tattern(self, *tracks: Track, channel: int = 0):
        """Set PTZ Tattern"""

        async for response in self._execute(
            self.commands.create_set_ptz_tatterns_request(channel, *tracks)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set PTZ Tattern failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Tattern failed")

    async def ptz_control(
        self,
        operation: Operation,
        speed: int | None = None,
        preset_id: int | None = None,
        channel: int = 0,
    ):
        """PTZ Control"""

        async for response in self._execute(
            self.commands.create_set_ptz_control_request(channel, operation, speed, preset_id)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set PTZ Control failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Control failed")

    async def get_ptz_autofocus_disabled(self, channel: int = 0):
        """Get PTZ AutoFocus"""

        async for response in self._execute(
            self.commands.create_get_ptz_autofocus_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_ptz_autofocus_response(response):
                return not response.disabled

            if self.commands.is_error(response):
                response.throw("Get PTZ AutoFocus failed")

        raise ReolinkResponseError("Get PTZ AutoFocus failed")

    async def set_ptz_autofocus(self, disabled: bool, channel: int = 0):
        """Set PTZ AutoFocus"""

        async for response in self._execute(
            self.commands.create_set_ptz_autofocus_request(channel, disabled)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set PTZ AutoFocus failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ AutoFocus failed")

    async def get_ptz_zoom_focus(self, channel: int = 0):
        """Get PTZ Zoom and Focus"""

        async for response in self._execute(
            self.commands.create_get_ptz_zoom_focus_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_ptz_zoom_focus_response(response):
                return response.state

            if self.commands.is_error(response):
                response.throw("Get PTZ Zoom Focus failed")

        raise ReolinkResponseError("Get PTZ Zoom Focus failed")

    async def set_ptz_zoom_focus(
        self,
        position: int,
        operation: ZoomOperation = ZoomOperation.ZOOM,
        channel: int = 0,
    ):
        """Set PTZ Zoom"""

        async for response in self._execute(
            self.commands.create_set_ptz_zoom_focus_request(channel, operation, position)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set PTZ Zoom/Focus failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set PTZ Zoom/Focus failed")
