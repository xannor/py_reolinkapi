"""Alarm"""

from typing import Final, TypedDict
from typing_extensions import TypeGuard

from .commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
)
from . import connection


class Alarm:
    """Alarm Mixin"""

    async def get_md_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetMotionStateCommand(channel))
        else:
            return None

        state = next(
            filter(GetMotionStateCommand.is_response, responses), None)
        return state


class GetMdStateResponseValueType(TypedDict):
    """Get Motion State Response Value"""

    state: int


class GetMotionStateCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Motion State"""

    COMMAND: Final = "GetMdState"
    RESPONSE: Final = "state"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetMdStateResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetMdStateResponseValueType)
        )
