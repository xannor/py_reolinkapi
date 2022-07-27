"""PTZ 3.7"""

from dataclasses import dataclass
from typing import Annotated, Final, NamedTuple, TypedDict, TypeGuard

from backports.strenum import StrEnum

from .utils import EnsureDataFields, Updateable, afilter, alist, amap

from . import connection

from .commands import (
    CommandRequestWithParam,
    CommandChannelParameter,
    CommandRequestTypes,
    CommandResponseValue,
    async_trap_errors,
)

from .typing import IntBool, BoolState, validate_in, validate_length

PTZPresetId = Annotated[int, validate_in(range(1, 64))]
"""Integer within 1 and 64"""

PTZPresetName = Annotated[str, validate_length(31)]
"""String max length of 31"""


@dataclass
class PTZPreset(Updateable, EnsureDataFields):
    """PTZ Preset"""

    channel: int
    id: PTZPresetId
    name: PTZPresetName
    enable: BoolState | None = None


class PTZPresetType(TypedDict):
    """PTZ Preset"""

    channel: int
    enable: IntBool
    id: PTZPresetId
    name: PTZPresetName


PTZPatrolPresetDwellTime = Annotated[int, validate_in(range(1, 30))]
"""Dwell Time for preset of 1 to 30 seconds"""

PTZPatrolPresetSpeed = Annotated[int, validate_in(range(1, 64))]
"""Patrol speed for preset within 1 to 64"""


@dataclass
class PTZPatrolPreset(Updateable, EnsureDataFields):
    """PTZ Patrol Preset"""

    dwellTime: PTZPatrolPresetDwellTime
    id: PTZPresetId
    speed: PTZPatrolPresetSpeed


class PTZPatrolPresetType(TypedDict):
    """PTZ Patrol Preset"""

    dwellTime: PTZPatrolPresetDwellTime
    id: PTZPresetId
    speed: PTZPatrolPresetSpeed


PTZPatrolId = PTZPresetId
"""Integer within 1 and 64"""

PTZPatrolName = PTZPresetName
"""String max length of 31"""


@dataclass
class PTZPatrol(Updateable, EnsureDataFields):
    """PTZ Patrol"""

    channel: int
    enable: BoolState
    id: PTZPatrolId
    preset: PTZPatrolPreset


class PTZPatrolType(TypedDict):
    """PTZ Patrol"""

    channel: int
    enable: IntBool
    id: PTZPatrolId
    name: PTZPatrolName
    preset: PTZPatrolPresetType
    running: IntBool


class PTZOperation(StrEnum):
    """PTZ Operations"""

    STOP = "Stop"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    LEFT_UP = "LeftUp"
    LEFT_DOWN = "LeftDown"
    RIGHT_UP = "RightUp"
    RIGHT_DOWN = "RightDown"
    IRIS_SHRINK = "IrisDec"
    IRIS_ENLARGE = "IrisInc"
    ZOOM_OUT = "ZoomDec"
    ZOOM_IN = "ZoomInc"
    FOCUS_BACK = "FocusInc"
    FOCUS_FORWARD = "FocusDec"
    AUTO = "Auto"
    PATROL_START = "StartPatrol"
    PATROL_STOP = "StopPatrol"
    TO_PRESET = "ToPos"


PTZTrackId = Annotated[int, validate_in(range(1, 6))]
PTZTrackName = Annotated[str, validate_length(191)]


@dataclass
class PTZTrack(Updateable, EnsureDataFields):
    """PTZ Track"""

    id: PTZTrackId
    name: PTZTrackName | None = None
    enable: BoolState | None = None


class PTZTrackType(TypedDict):
    """PTZ Track"""

    enable: IntBool
    id: PTZTrackId
    name: PTZTrackName
    running: IntBool


class PTZAutoFocusType(TypedDict):
    """PTZ AutoFocus"""

    channel: int
    disable: IntBool


class PTZPositionType(TypedDict):
    """PTZ Position"""

    pos: int


class PTZZoomFocus(NamedTuple):
    """PTZ Zoom Focus Positions"""

    zoom: int
    focus: int


NO_ZOOM_FOCUS: Final = PTZZoomFocus(0, 0)


class PTZZoomFocusType(TypedDict):
    """PTZ Zoom Focus"""

    channel: int
    focus: PTZPositionType
    zoom: PTZPositionType


class PTZZoomOperation(StrEnum):

    ZOOM = "ZoomPos"
    FOCUS = "FocusPos"


class PTZ:
    """PTZ commands Mixin"""

    async def get_ptz_presets(self, channel: int = 0):
        """Get PTZ Presets"""

        Command = GetPTZPresetCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command(channel)))
        else:
            return []

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        return result or []

    async def set_ptz_preset(self, preset: PTZPreset):
        """Set PTZ Preset"""
        Command = SetPTZPresetCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(preset)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def get_ptz_patrols(self, channel: int = 0):
        """Get PTZ Patrols"""

        Command = GetPTZPatrolCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command(channel)))
        else:
            return []

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        return result or []

    async def set_ptz_patrol(self, preset: PTZPatrol):
        """Set PTZ Patrol"""
        Command = SetPTZPatrolCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(preset)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def ptz_control(self, operation: PTZOperation, speed: PTZPatrolPresetSpeed | None = None, preset_id: PTZPresetId | None = None, channel: int = 0):
        """PTZ Control"""
        Command = PTZControlCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(operation, preset_id, speed, channel)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def get_ptz_tatterns(self, channel: int = 0):
        """Get PTZ Tatterns"""

        Command = GetPTZTatternCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command(channel)))
        else:
            return []

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        return result or []

    async def set_ptz_tattern(self, *tracks: PTZTrack, channel: int = 0):
        """Set PTZ Tattern"""
        Command = SetPTZTatternCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(*tracks, channel=channel)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def get_ptz_autofocus(self, channel: int = 0):
        """Get PTZ AutoFocus"""

        Command = GetPTZAutoFocusCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command(channel)))
        else:
            return False

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        if result is not None:
            return not result["disable"]
        return False

    async def set_ptz_autofocus(self, disabled: bool, channel: int = 0):
        """Set PTZ AutoFocus"""
        Command = SetPTZAutoFocusCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(channel, disabled)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def get_ptz_zoom_focus(self, channel: int = 0):
        """Get PTZ Zoom and Focus"""

        Command = GetPTZZoomFocusCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command(channel)))
        else:
            return NO_ZOOM_FOCUS

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        if result is not None:
            return PTZZoomFocus(result["zoom"]["pos"], result["focus"]["pos"])
        return NO_ZOOM_FOCUS

    async def set_ptz_zoom(self, position: int, channel: int = 0):
        """Set PTZ Zoom"""
        Command = StartPTZZoomFocusCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(PTZZoomOperation.ZOOM, position, channel)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True

    async def set_ptz_focus(self, position: int, channel: int = 0):
        """Set PTZ Focus"""
        Command = StartPTZZoomFocusCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(PTZZoomOperation.FOCUS, position, channel)
            ))
        else:
            return False

        await alist(responses)  # eat all results looking for errors
        return True


class GetPTZPresetResponseType(TypedDict):
    """Get PTZ Presets Response"""

    PtzPreset: list[PTZPresetType]


class GetPTZPresetCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get PTZ Presets"""

    COMMAND: Final = "GetPtzPreset"
    RESPONSE: Final = "PtzPreset"

    def __init__(
        self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetPTZPresetResponseType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetPTZPresetResponseType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetPTZPresetResponseType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


@dataclass
class SetPTZPresetParameter:
    """Set PTZ Preset"""

    PtzPreset: PTZPreset


class SetPTZPresetCommand(CommandRequestWithParam[SetPTZPresetParameter]):
    """Set PTZ Preset"""

    COMMAND: Final = "SetPtzPreset"

    def __init__(self, preset: PTZPreset, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action,
                         SetPTZPresetParameter(preset))


class GetPTZPatrolResponseType(TypedDict):
    """Get PTZ Patrol Response"""

    PtzPatrol: list[PTZPatrolType]


class GetPTZPatrolCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get PTZ Patrol"""

    COMMAND: Final = "GetPtzPatrol"
    RESPONSE: Final = "PtzPatrol"

    def __init__(
        self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetPTZPatrolResponseType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetPTZPatrolResponseType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetPTZPatrolResponseType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


@dataclass
class SetPTZPatrolParameter:
    """Set PTZ Patrol"""

    PtzPatrol: PTZPatrol


class SetPTZPatrolCommand(CommandRequestWithParam[SetPTZPatrolParameter]):
    """Set PTZ Patrol"""

    COMMAND: Final = "SetPtzPreset"

    def __init__(self, patrol: PTZPatrol, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action,
                         SetPTZPatrolParameter(patrol))


@dataclass
class PTZControlParameter(CommandChannelParameter):
    """PTZ Control"""

    op: PTZOperation
    id: PTZPresetId | None = None
    speed: PTZPatrolPresetSpeed | None = None


class PTZControlCommand(CommandRequestWithParam[PTZControlParameter]):
    """PTZ Control"""

    COMMAND: Final = "PtzCtrl"

    def __init__(self, operation: PTZOperation, preset_id: PTZPresetId | None = None, speed: PTZPatrolPresetSpeed | None = None, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action,
                         PTZControlParameter(channel, operation, preset_id, speed))


class GetPTZTatternResponseType(TypedDict):
    """Get PTZ Tattern Response"""

    PtzTattern: list[PTZTrackType]


class GetPTZTatternCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get PTZ Tattern"""

    COMMAND: Final = "GetPtzTattern"
    RESPONSE: Final = "PtzTattern"

    def __init__(
        self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetPTZTatternResponseType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetPTZTatternResponseType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetPTZTatternResponseType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


@dataclass
class SetPTZTatternTatternParameter(CommandChannelParameter):
    """Set PTZ Tattern Parameter"""

    track: list[PTZTrack]


@dataclass
class SetPTZTatternParameter:
    """Set PTZ Tattern"""

    PtzTattern: SetPTZTatternTatternParameter


class SetPTZTatternCommand(CommandRequestWithParam[SetPTZTatternParameter]):
    """Set PTZ Tattern"""

    COMMAND: Final = "SetPtzTattern"

    def __init__(self, *tracks: PTZTrack, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action,
                         SetPTZTatternParameter(SetPTZTatternTatternParameter(channel, tracks)))


class GetPTZAutoFocusResponseType(TypedDict):
    """Get PTZ AutoFocus Response"""

    AutoFocus: PTZAutoFocusType


class GetPTZAutoFocusCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get PTZ AutoFocus"""

    COMMAND: Final = "GetAutoFocus"
    RESPONSE: Final = "AutoFocus"

    def __init__(
        self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetPTZAutoFocusResponseType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetPTZAutoFocusResponseType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetPTZAutoFocusResponseType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


@dataclass
class SetPTZAutoFocusAtoFocusParameter(CommandChannelParameter):
    """Set PTZ AutoFocus"""

    disable: BoolState


@dataclass
class SetPTZAutoFocusParameter:
    """Set PTZ AutoFocus"""

    AutoFocus: SetPTZAutoFocusAtoFocusParameter


class SetPTZAutoFocusCommand(CommandRequestWithParam[SetPTZAutoFocusParameter]):
    """Set PTZ Preset"""

    COMMAND: Final = "SetAutoFocus"

    def __init__(self, disabled: BoolState, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action,
                         SetPTZAutoFocusParameter(SetPTZAutoFocusAtoFocusParameter(channel, disabled)))


class GetPTZZoomFocusResponseType(TypedDict):
    """Get PTZ Zoom/Focus Response"""

    ZoomFocus: PTZZoomFocusType


class GetPTZZoomFocusCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get PTZ Zoom and Focus"""

    COMMAND: Final = "GetZoomFocus"
    RESPONSE: Final = "ZoomFocus"

    def __init__(
        self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetPTZZoomFocusResponseType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetPTZZoomFocusResponseType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetPTZZoomFocusResponseType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


@dataclass
class _StartPTZZoomFocusParameter:

    @dataclass
    class _ZoomFocus(CommandChannelParameter):
        pos: int
        op: PTZZoomOperation

    ZoomFocus: _ZoomFocus


class StartPTZZoomFocusCommand(CommandRequestWithParam[_StartPTZZoomFocusParameter]):
    """Set PTZ Zoom or Focus"""

    COMMAND: Final = "StartZoomFocus"

    def __init__(self, operation: PTZZoomOperation, position: int, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, _StartPTZZoomFocusParameter(
            _StartPTZZoomFocusParameter._ZoomFocus(channel, position, operation)))
