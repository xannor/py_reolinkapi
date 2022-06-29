"""Encoding"""

from typing import Final, TypedDict
from typing_extensions import TypeGuard

from .commands import CommandChannelParameter, CommandRequestTypes, CommandRequestWithParam
from . import connection


class StreamEncodingInfo(TypedDict):
    """Encoding Info"""

    bitRate: int
    frameRate: int
    gop: int
    height: int
    width: int
    profile: str
    size: str
    vType: str


class EncodingInfo(TypedDict):
    """Encoding Info"""

    audio: bool
    channel: int
    mainStream: StreamEncodingInfo
    subStream: StreamEncodingInfo
    extStream: StreamEncodingInfo


class Encoding:
    """Encoding Mixin"""

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                GetEncodingCommand(channel)
            )
        else:
            return None

        return next(filter(GetEncodingCommand.is_response, responses), None)


class GetEncodingResponseValueType(TypedDict):
    """Get Encoding Response Value"""

    Enc: EncodingInfo


class GetEncodingCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Encoding"""

    COMMAND: Final = "GetEnc"
    RESPONSE: Final = "Enc"

    def __init__(self, channel: int = 0, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetEncodingResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetEncodingResponseValueType)
        )
