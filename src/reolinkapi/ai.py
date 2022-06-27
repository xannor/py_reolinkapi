"""AI"""

from enum import Enum
from typing import Final, Iterable, TypedDict

from .commands import COMMAND, COMMAND_RESPONSE_VALUE, CommandChannelParameter, CommandRequestTypes, CommandRequestWithParam, CommandResponse, create_value_has_key, isvalue
from . import connection

class AITypes(str, Enum):
    """AI Types"""

    ANIMAL = "animal"
    PET = "dog_cat"
    FACE = "face"
    PEOPLE = "people"
    VEHICLE = "vehicle"


class AiAlarmState(TypedDict):
    """AI Response State"""

    alarm_state: int
    support: int

class AI:
    """AI Mixin"""

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetAiStateRequest(channel))
        else:
            return None

        state = next(GetAiStateRequest.get_responses(responses), None)
        return state

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetAiConfigRequest(channel))
        else:
            return None

        config = next(GetAiConfigRequest.get_responses(responses), None)
        return config

class GetAiStateResponseValue(TypedDict, total=False):
    """Get AI State Response Value"""

    channel: int
    dog_cat: AiAlarmState
    face: AiAlarmState
    people: AiAlarmState
    vehicle: AiAlarmState

class GetAiStateRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get AI State"""

    COMMAND:Final = "GetAiState"
    RESPONSE:Final = "channel"

    def __init__(self, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))
        
    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """Get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE],
            filter(
                _isAiState,
                filter(
                    isvalue,
                    filter(
                        lambda response: response[COMMAND] == cls.COMMAND,
                        responses,
                    ),
                ),
            ),
        )


_isAiState = create_value_has_key(
    GetAiStateRequest.RESPONSE, GetAiStateResponseValue, int
)

class GetAiConfigResponseValue(TypedDict, total=False):
    """Get AI Config Response Value"""

    channel: int
    AiDetectType: dict[AITypes, int]
    aiTrack: int
    trackType: dict[AITypes, int]

class GetAiConfigRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get AI Config"""

    COMMAND:Final = "GetAiCfg"
    RESPONSE:Final = "channel"

    def __init__(self, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))
        
    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """Get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE],
            filter(
                _isAiConfig,
                filter(
                    isvalue,
                    filter(
                        lambda response: response[COMMAND] == cls.COMMAND,
                        responses,
                    ),
                ),
            ),
        )


_isAiConfig = create_value_has_key(
    GetAiConfigRequest.RESPONSE, GetAiConfigResponseValue, int
)
