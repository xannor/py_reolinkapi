"""Encoding"""

from typing import Final, Iterable, TypedDict

from .commands import COMMAND, COMMAND_RESPONSE_VALUE, CommandChannelParameter, CommandRequestTypes, CommandRequestWithParam, CommandResponse, create_value_has_key, isvalue
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
                GetEncodingRequest(channel)
            )
        else:
            return None

        return next(GetEncodingRequest.get_responses(responses), None)

class GetEncodingResponseValue(TypedDict):
    """Get Encoding Response Value"""

    Enc: EncodingInfo

class GetEncodingRequest(CommandRequestWithParam[CommandChannelParameter]):
    """Get Encoding"""
    
    COMMAND: Final = "GetEnc"
    RESPONSE:Final = "Enc"

    def __init__(self, channel:int = 0, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action, CommandChannelParameter(channel))

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """Get responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isEncoding,
                filter(
                    isvalue,
                    filter(
                        lambda response: response[COMMAND] == cls.COMMAND, responses
                    ),
                ),
            ),
        )


_isEncoding = create_value_has_key(GetEncodingRequest.RESPONSE, GetEncodingResponseValue)
