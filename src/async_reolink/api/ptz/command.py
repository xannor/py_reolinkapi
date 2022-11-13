"""PTZ Commands"""

from typing import Annotated, Mapping, MutableSequence, Protocol

from ..connection.typing import ChannelValue
from .typing import Operation, Patrol, Preset, Track, ZoomFocus, ZoomOperation


class GetPresetRequest(ChannelValue, Protocol):
    """Get Presets Request"""


class GetPresetResponse(ChannelValue, Protocol):
    """Get Presets Response"""

    presets: Mapping[int, Preset]


class SetPresetRequest(Protocol):
    """Set Preset Request"""

    preset: Preset


class GetPatrolRequest(ChannelValue, Protocol):
    """Get Patrol"""


class GetPatrolResponse(ChannelValue, Protocol):
    """Get Patrol Response"""

    patrols: Mapping[int, Patrol]


class SetPatrolRequest(Protocol):
    """Set  Patrol"""

    patrol: Patrol


class SetControlRequest(ChannelValue, Protocol):
    """PTZ Control"""

    operation: Operation
    preset_id: int | None
    speed: Annotated[int, range(1, 64)] | None
    """Patrol speed for preset within 1 to 64"""


class GetTatternRequest(ChannelValue, Protocol):
    """Get Tattern"""


class GetTatternResponse(ChannelValue, Protocol):
    """Get Tattern Response"""

    tracks: Mapping[int, Track]


class SetTatternRequest(ChannelValue, Protocol):
    """Set PTZ Tattern"""

    tracks: MutableSequence[Track]


class GetAutoFocusRequest(ChannelValue, Protocol):
    """Get PTZ AutoFocus"""


class GetAutoFocusResponse(ChannelValue, Protocol):
    """Get PTZ Presets Response"""

    disabled: bool


class SetAutoFocusRequest(ChannelValue, Protocol):
    """Set PTZ Preset"""

    disabled: bool


class GetZoomFocusRequest(ChannelValue, Protocol):
    """Get Zoom and Focus"""


class GetZoomFocusResponse(ChannelValue, Protocol):
    """Get Zoom/Focus Response"""

    state: ZoomFocus


class SetZoomFocusRequest(ChannelValue, Protocol):
    """Set Zoom or Focus"""

    operation: ZoomOperation
    position: int
