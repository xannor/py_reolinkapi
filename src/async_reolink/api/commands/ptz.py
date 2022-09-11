"""PTZ Commands"""

from abc import ABC
from typing import Annotated, Mapping, MutableSequence

from ..ptz.typings import Operation, Preset, Patrol, Track, ZoomOperation
from . import CommandRequest, ChannelValue, CommandResponse


class GetPresetRequest(CommandRequest, ChannelValue, ABC):
    """Get Presets Request"""


class GetPresetResponse(CommandResponse, ABC):
    """Get Presets Response"""

    presets: Mapping[int, Preset]


class SetPresetRequest(CommandRequest, ABC):
    """Set Preset Request"""

    preset: Preset


class GetPatrolRequest(CommandRequest, ChannelValue, ABC):
    """Get Patrol"""


class GetPatrolResponse(CommandResponse, ABC):
    """Get Patrol Response"""

    patrols: Mapping[int, Patrol]


class SetPatrolRequest(CommandRequest, ABC):
    """Set  Patrol"""

    patrol: Patrol


class SetControlRequest(CommandRequest, ChannelValue, ABC):
    """PTZ Control"""

    operation: Operation
    preset_id: int | None
    speed: Annotated[int, range(1, 64)] | None
    """Patrol speed for preset within 1 to 64"""


class GetTatternRequest(CommandRequest, ChannelValue, ABC):
    """Get Tattern"""


class GetTatternResponse(CommandResponse, ChannelValue, ABC):
    """Get Tattern Response"""

    tracks: Mapping[int, Track]


class SetTatternRequest(CommandRequest, ChannelValue, ABC):
    """Set PTZ Tattern"""

    tracks: MutableSequence[Track]


class GetAutoFocusRequest(CommandRequest, ChannelValue, ABC):
    """Get PTZ AutoFocus"""


class GetAutoFocusResponse(CommandResponse, ChannelValue, ABC):
    """Get PTZ Presets Response"""

    disabled: bool


class SetAutoFocusRequest(CommandRequest, ChannelValue, ABC):
    """Set PTZ Preset"""

    disabled: bool


class GetZoomFocusRequest(CommandRequest, ChannelValue, ABC):
    """Get Zoom and Focus"""


class GetZoomFocusResponse(CommandResponse, ChannelValue, ABC):
    """Get Zoom/Focus Response"""

    focus: Annotated[int, range(1, 64)]
    zoom: Annotated[int, range(1, 64)]


class SetZoomFocusRequest(CommandRequest, ChannelValue, ABC):
    """Set Zoom or Focus"""

    operation: ZoomOperation
    position: int
