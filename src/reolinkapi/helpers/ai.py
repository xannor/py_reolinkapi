"""AI Helpers"""

from typing import Final, Iterable, TypedDict

from ..models.ai import AITypes

from ..typings.commands import (
    COMMAND,
    COMMAND_RESPONSE_VALUE,
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)

from ..typings.ai import AiAlarmState

from . import commands as commandHelpers


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


class GetAiConfigResponseValue(TypedDict, total=False):
    """Get AI Config Response Value"""

    channel: int
    AiDetectType: dict[AITypes, int]
    aiTrack: int
    trackType: dict[AITypes, int]


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


def get_ai_state_responses(responses: Iterable[CommandResponse]):
    """Get AI States from responses"""
    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE],
        filter(
            _isAiState,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response[COMMAND] == GET_AI_STATE_COMMAND,
                    responses,
                ),
            ),
        ),
    )


GET_AI_CONFIG_COMMAND: Final = "GetAiCfg"

_isAiConfig = commandHelpers.create_value_has_key(
    "channel", GetAiConfigResponseValue, int
)


def get_ai_config_responses(responses: Iterable[CommandResponse]):
    """Get AI Config from responses"""
    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE],
        filter(
            _isAiConfig,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response[COMMAND] == GET_AI_CONFIG_COMMAND,
                    responses,
                ),
            ),
        ),
    )


def create_get_ai_config(
    channel: int = 0,
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create AI Config Request"""
    return CommandRequestWithParam(
        cmd=GET_AI_CONFIG_COMMAND,
        action=_type,
        param=CommandChannelParameter(channel=channel),
    )
