"""Alarm"""

from typing import Final, TypedDict, TypeGuard

from .utils import afilter, amap


from .typing import OnOffState

from .commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponseValue,
    async_trap_errors,
)
from . import connection


class Alarm:
    """Alarm Mixin"""

    async def get_md_state(self, channel: int = 0):
        """Get AI State Info"""

        Command = GetMotionStateCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(
                Command(channel)
            ))
        else:
            return None

        result = await anext(
            amap(
                Command.get_value,
                afilter(
                    Command.is_response,
                    responses
                )
            ),
            None,
        )

        if result is not None:
            return OnOffState(result)
        return None


class GetMdStateResponseValueType(TypedDict):
    """Get Motion State Response Value"""

    state: int


class GetMotionStateCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Motion State"""

    COMMAND: Final = "GetMdState"
    RESPONSE: Final = "state"

    def __init__(
        self,
        channel: int = 0,
        action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetMdStateResponseValueType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(value, cls.RESPONSE, GetMdStateResponseValueType)

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetMdStateResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]
