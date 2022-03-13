"""Alarm Commands"""

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


class GetMdStateResponseValue(TypedDict):
    """Get Motion State Response Value"""

    state: int


GET_MD_STATE_COMMAND: Final = "GetMdState"

_isMdState = commandHelpers.create_value_has_key("state", GetMdStateResponseValue, int)


def _get_md_state_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"]["state"],
        filter(
            _isMdState,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_MD_STATE_COMMAND, responses
                ),
            ),
        ),
    )


class Alarm:
    """Alarm Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        other: any = self
        if isinstance(other, connection.Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = other._execute

    @staticmethod
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

    @staticmethod
    def get_md_state_responses(responses: Iterable[CommandResponse]):
        """Get AI State Responses"""

        return _get_md_state_responses(responses)

    async def get_md_state(self, channel: int = 0):
        """Get AI State Info"""

        state = next(
            _get_md_state_responses(
                await self._execute(Alarm.create_get_md_state(channel))
            ),
            None,
        )
        return state
