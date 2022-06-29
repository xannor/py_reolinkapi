"""AI"""

from typing import Final, TypedDict
from typing_extensions import TypeGuard

try:
    from enum import StrEnum  # pylint: disable=ungrouped-imports
except ImportError:
    from backports.strenum import StrEnum

from .commands import CommandChannelParameter, CommandRequestTypes, CommandRequestWithParam
from . import connection


class AITypes(StrEnum):
    """AI Types"""

    ANIMAL = "animal"
    PET = "dog_cat"
    FACE = "face"
    PEOPLE = "people"
    VEHICLE = "vehicle"


class AiAlarmStateType(TypedDict):
    """AI Response State"""

    alarm_state: int
    support: int


class AI:
    """AI Mixin"""

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetAiStateCommand(channel))
        else:
            return None

        state = next(filter(GetAiStateCommand.is_response, responses), None)
        return state

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetAiConfigCommand(channel))
        else:
            return None

        config = next(filter(GetAiConfigCommand.is_response, responses), None)
        return config


class GetAiStateResponseValueType(TypedDict, total=False):
    """Get AI State Response Value"""

    channel: int
    dog_cat: AiAlarmStateType
    face: AiAlarmStateType
    people: AiAlarmStateType
    vehicle: AiAlarmStateType


class GetAiStateCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get AI State"""

    COMMAND: Final = "GetAiState"
    RESPONSE: Final = "channel"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetAiStateResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetAiStateResponseValueType)
        )


class GetAiConfigResponseValueType(TypedDict, total=False):
    """Get AI Config Response Value"""

    channel: int
    AiDetectType: dict[AITypes, int]
    aiTrack: int
    trackType: dict[AITypes, int]


class GetAiConfigCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get AI Config"""

    COMMAND: Final = "GetAiCfg"
    RESPONSE: Final = "channel"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetAiConfigResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetAiConfigResponseValueType)
        )
