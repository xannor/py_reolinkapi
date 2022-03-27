"""Alarm Helpers"""

from typing import Final, Iterable, TypedDict

from ..typings.commands import (
    COMMAND,
    COMMAND_RESPONSE_VALUE,
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)

from . import commands as commandHelpers


class GetMdStateResponseValue(TypedDict):
    """Get Motion State Response Value"""

    state: int


GET_MD_STATE_COMMAND: Final = "GetMdState"

_isMdState = commandHelpers.create_value_has_key("state", GetMdStateResponseValue, int)


def get_md_state_responses(responses: Iterable[CommandResponse]):
    """Get Motion State from responses"""
    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["state"],
        filter(
            _isMdState,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response[COMMAND] == GET_MD_STATE_COMMAND,
                    responses,
                ),
            ),
        ),
    )


def create_get_md_state(
    channel: int = 0,
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create Motion State Request"""
    return CommandRequestWithParam(
        cmd=GET_MD_STATE_COMMAND,
        action=_type,
        param=CommandChannelParameter(channel=channel),
    )
