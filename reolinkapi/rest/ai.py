"""AI Commands"""
from __future__ import annotations
from typing import Final, Iterable, TypedDict

from ..typings.commands import (
    CommandChannelParameter,
    CommandRequestWithParam,
    CommandRequestTypes,
    CommandResponse,
)

from ..helpers import commands as commandHelpers

from . import connection


class AiAlarmState(TypedDict):
    """AI Response State"""

    alarm_state: int
    support: int


class GetAiStateResponseValue(TypedDict, total=False):
    """Get AI State Response Value"""

    channel: int
    dog_cat: AiAlarmState
    face: AiAlarmState
    people: AiAlarmState
    vehicle: AiAlarmState


GET_AI_STATE_COMMAND: Final = "GetAiState"

_isAiState = commandHelpers.create_value_has_key(
    "channel", GetAiStateResponseValue, int
)


def _get_ai_state_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"],
        filter(
            _isAiState,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_AI_STATE_COMMAND, responses
                ),
            ),
        ),
    )


class AI:
    """AI Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        other: any = self
        if isinstance(other, connection.Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = other._execute

    @staticmethod
    def create_get_ai_state(
        channel: int = 0,
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create AI State Request"""
        return CommandRequestWithParam(
            cmd=GET_AI_STATE_COMMAND,
            action=_type,
            param=CommandChannelParameter(channel=channel),
        )

    @staticmethod
    def get_ai_state_responses(responses: Iterable[CommandResponse]):
        """Get AI State Responses"""

        return _get_ai_state_responses(responses)

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        state = next(
            _get_ai_state_responses(
                await self._execute(AI.create_get_ai_state(channel))
            ),
            None,
        )
        return state
