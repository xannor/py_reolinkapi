"""Encoding"""

from typing import Final, TypedDict, TypeGuard

from .utils import afilter, amap

from .commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponseValue,
    async_trap_errors,
)
from . import connection

from .typing import OnOffState


class StreamEncodingInfoType(TypedDict):
    """Encoding Info"""

    bitRate: int
    frameRate: int
    gop: int
    height: int
    width: int
    profile: str
    size: str
    vType: str


class EncodingInfoType(TypedDict):
    """Encoding Info"""

    audio: OnOffState
    channel: int
    mainStream: StreamEncodingInfoType
    subStream: StreamEncodingInfoType
    extStream: StreamEncodingInfoType


class Encoding:
    """Encoding Mixin"""

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        Command = GetEncodingCommand

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

        return result


class GetEncodingResponseValueType(TypedDict):
    """Get Encoding Response Value"""

    Enc: EncodingInfoType


class GetEncodingCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Encoding"""

    COMMAND: Final = "GetEnc"
    RESPONSE: Final = "Enc"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[CommandResponseValue[GetEncodingResponseValueType]]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetEncodingResponseValueType)
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetEncodingResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]
