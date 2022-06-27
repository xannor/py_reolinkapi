"""Alarm"""

from typing import Final, Iterable, TypedDict
from .commands import COMMAND, COMMAND_RESPONSE_VALUE, CommandChannelParameter, CommandRequestTypes, CommandRequestWithParam, CommandResponse, create_value_has_key, isvalue
from . import connection

class Alarm:
    """Alarm Mixin"""

    async def get_md_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetMotionStateRequest(channel))
        else:
            return None

        state = next(GetMotionStateRequest.get_responses(responses), None)
        return state

class GetMdStateResponseValue(TypedDict):
    """Get Motion State Response Value"""

    state: int

class GetMotionStateRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get Motion State"""

    COMMAND: Final = "GetMdState"
    RESPONSE: Final = "state"

    def __init__(self, channel:int=0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """Get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isMdState,
                filter(
                    isvalue,
                    filter(
                        lambda response: response[COMMAND] == cls.COMMAND,
                        responses,
                    ),
                ),
            ),
        )

_isMdState = create_value_has_key(GetMotionStateRequest.RESPONSE, GetMdStateResponseValue, int)
