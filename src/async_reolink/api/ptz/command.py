"""PTZ Commands"""

from typing import Annotated, Mapping, MutableSequence, Protocol, TypeGuard

from ..connection.typing import ChannelValue
from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from .typing import Operation, Patrol, Preset, Track, ZoomFocus, ZoomOperation


class GetPresetRequest(CommandRequest, ChannelValue, Protocol):
    """Get Presets Request"""


class GetPresetResponse(CommandResponse, ChannelValue, Protocol):
    """Get Presets Response"""

    presets: Mapping[int, Preset]


class SetPresetRequest(CommandRequest, Protocol):
    """Set Preset Request"""

    preset: Preset


class GetPatrolRequest(CommandRequest, ChannelValue, Protocol):
    """Get Patrol"""


class GetPatrolResponse(CommandResponse, ChannelValue, Protocol):
    """Get Patrol Response"""

    patrols: Mapping[int, Patrol]


class SetPatrolRequest(CommandRequest, Protocol):
    """Set  Patrol"""

    patrol: Patrol


class SetControlRequest(CommandRequest, ChannelValue, Protocol):
    """PTZ Control"""

    operation: Operation
    preset_id: int | None
    speed: Annotated[int, range(1, 64)] | None
    """Patrol speed for preset within 1 to 64"""


class GetTatternRequest(CommandRequest, ChannelValue, Protocol):
    """Get Tattern"""


class GetTatternResponse(CommandResponse, ChannelValue, Protocol):
    """Get Tattern Response"""

    tracks: Mapping[int, Track]


class SetTatternRequest(CommandRequest, ChannelValue, Protocol):
    """Set PTZ Tattern"""

    tracks: MutableSequence[Track]


class GetAutoFocusRequest(CommandRequest, ChannelValue, Protocol):
    """Get PTZ AutoFocus"""


class GetAutoFocusResponse(CommandResponse, ChannelValue, Protocol):
    """Get PTZ Presets Response"""

    disabled: bool


class SetAutoFocusRequest(CommandRequest, ChannelValue, Protocol):
    """Set PTZ Preset"""

    disabled: bool


class GetZoomFocusRequest(CommandRequest, ChannelValue, Protocol):
    """Get Zoom and Focus"""


class GetZoomFocusResponse(CommandResponse, ChannelValue, Protocol):
    """Get Zoom/Focus Response"""

    state: ZoomFocus


class SetZoomFocusRequest(CommandRequest, ChannelValue, Protocol):
    """Set Zoom or Focus"""

    operation: ZoomOperation
    position: int


class CommandFactory(WithCommandFactory, Protocol):
    """PTZ Command Factory"""

    def create_get_ptz_presets_request(self, channel_id: int) -> GetPresetRequest:
        """create GetPresetRequest"""

    def is_get_ptz_presets_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetPresetResponse]:
        """is GetPresetResponse"""

    def create_set_ptz_preset_request(
        self, channel_id: int, preset: Preset
    ) -> SetPresetRequest:
        """create SetPresetRequest"""

    def create_get_ptz_patrols_request(self, channel_id: int) -> GetPatrolRequest:
        """create GetPatrolRequest"""

    def is_get_ptz_patrols_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetPatrolResponse]:
        """is GetPatrolResponse"""

    def create_set_ptz_patrol_request(
        self, channel_id: int, patrol: Patrol
    ) -> SetPatrolRequest:
        """create SetPatrolRequest"""

    def create_get_ptz_tatterns_request(self, channel_id: int) -> GetTatternRequest:
        """create GetTatternRequest"""

    def is_get_ptz_tatterns_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetTatternResponse]:
        """is GetTatternResponse"""

    def create_set_ptz_tatterns_request(
        self, channel_id: int, *track: Track
    ) -> SetTatternRequest:
        """create SetTatternRequest"""

    def create_set_ptz_control_request(
        self,
        channel_id: int,
        operation: Operation,
        speed: int | None,
        preset_id: int | None,
    ) -> SetControlRequest:
        """create SetControlRequest"""

    def create_get_ptz_autofocus_request(self, channel_id: int) -> GetAutoFocusRequest:
        """create GetAutoFocusRequest"""

    def is_get_ptz_autofocus_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetAutoFocusResponse]:
        """is GetAutoFocusResponse"""

    def create_set_ptz_autofocus_request(
        self, channel_id: int, disabled: bool
    ) -> SetAutoFocusRequest:
        """create SetAutoFocusRequest"""

    def create_get_ptz_zoom_focus_request(self, channel_id: int) -> GetZoomFocusRequest:
        """create GetZoomFocusRequest"""

    def is_get_ptz_zoom_focus_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetZoomFocusResponse]:
        """is GetZoomFocusResponse"""

    def create_set_ptz_zoomfocus_request(
        self, channel_id: int, operation: ZoomOperation, position: int
    ) -> SetZoomFocusRequest:
        """create SetZoomFocusRequest"""
