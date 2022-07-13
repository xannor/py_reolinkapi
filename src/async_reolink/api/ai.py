"""AI"""

from __future__ import annotations
from enum import auto

from typing import Final, Mapping, NewType, TypedDict
from typing_extensions import TypeGuard

from .typing import BoolState, OnOffState, StrEnum

from .utils import afilter, amap

from .commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponseValue,
    CommandResponseChannelValueType,
    async_trap_errors,
)
from . import connection


GetAiStateResponseValueType = NewType(
    "GetAiStateResponseValueType", CommandResponseChannelValueType
)


class AITypes(StrEnum):
    """AI Types"""

    ANIMAL = auto()
    PET = "dog_cat"
    FACE = auto()
    PEOPLE = auto()
    VEHICLE = auto()

    @staticmethod
    def is_ai_response_values(
        _response: GetAiConfigResponseValueType,
    ) -> TypeGuard[Mapping[AITypes, AiAlarmStateType]]:
        """cast to mapping"""
        return True


class AiAlarmStateType(TypedDict, total=False):
    """AI Response State"""

    alarm_state: OnOffState
    support: BoolState


class AI:
    """AI Mixin"""

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        Command = GetAiStateCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command(channel)))
        else:
            return None

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )
        if AITypes.is_ai_response_values(result):
            return result
        return None

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        Command = GetAiConfigCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command(channel)))
        else:
            return None

        result = await anext(
            afilter(Command.is_response, responses),
            None,
        )
        return result


class GetAiStateCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get AI State"""

    COMMAND: Final = "GetAiState"
    RESPONSE: Final = "channel"

    def __init__(
        self,
        channel: int = 0,
        action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[
        CommandResponseValue[GetAiStateResponseValueType]
    ]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(value, cls.RESPONSE, GetAiStateResponseValueType)


class GetAiConfigResponseValueType(CommandResponseChannelValueType, total=False):
    """Get AI Config Response Value"""

    AiDetectType: dict[AITypes, int]
    aiTrack: int
    trackType: dict[AITypes, int]


class GetAiConfigCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get AI Config"""

    COMMAND: Final = "GetAiCfg"
    RESPONSE: Final = "channel"

    def __init__(
        self,
        channel: int = 0,
        action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[GetAiConfigResponseValueType]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(value, cls.RESPONSE, GetAiConfigResponseValueType)
