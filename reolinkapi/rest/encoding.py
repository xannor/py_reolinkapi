""" Encoding Commands """

from dataclasses import dataclass, field
from typing import ClassVar, Union

from reolinkapi.rest.const import StreamTypes

from reolinkapi.utils.mappings import Wrapped

from ..utils.dataclasses import flatten, keyword

from .command import (
    CommandRequest,
    CommandRequestChannelParam,
    CommandValueResponse,
    CommandValueResponseValue,
    response_type,
)
from ..meta.connection import ConnectionInterface


@dataclass
class StreamEncodingInfo:
    """Encoding Info"""

    bit_rate: int = field(default=0, metadata=keyword("bitRate"))
    frame_rate: int = field(default=0, metadata=keyword("frameRate"))
    gop: int = field(default=0)
    height: int = field(default=0)
    width: int = field(default=0)
    profile: str = field(default="")
    size: str = field(default="")
    video_type: str = field(default="", metadata=keyword("vType"))


class StreamsEncoding(Wrapped[StreamTypes, StreamEncodingInfo]):
    """Streams Encoding"""

    def update(self, *args, **kwargs):
        def _make_key(key: Union[StreamTypes, str, int]):
            if isinstance(key, str):
                if key[-6:] != "Stream":
                    raise KeyError(key)
                key = key[0:6].upper()
                return StreamTypes[key]
            return StreamTypes(key)

        super.update(
            *((_make_key(k), v) for k, v in args),
            **{_make_key(k): v for k, v in kwargs.items()}
        )


@dataclass
class EncodingInfo:
    """Encoding Info"""

    audio: bool = field(default=False)
    channel: int = field(default=0)
    streams: StreamsEncoding = field(
        default_factory=StreamsEncoding, metadata=flatten()
    )


@dataclass
class GetEncodingResponseValue(CommandValueResponseValue):
    """Get Encoding Response Value"""

    info: EncodingInfo = field(default_factory=EncodingInfo, metadata=keyword("Enc"))


@dataclass
class GetEncodingResponse(CommandValueResponse):
    """Get Encoding Response"""

    value: GetEncodingResponseValue = field(default_factory=GetEncodingResponseValue)


@dataclass
@response_type(GetEncodingResponse)
class GetEncodingRequest(CommandRequest):
    """Get Encoding Request"""

    COMMAND: ClassVar = "GetEnc"
    param: CommandRequestChannelParam = field(
        default_factory=CommandRequestChannelParam
    )

    def __post_init__(self):
        self.command = type(self).COMMAND


class Encoding:
    """Encoding Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, ConnectionInterface) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute

    async def get_rtsp_url(self, channel: int = 0):
        """Get RTSP Url"""

        results = await self._execute(
            GetEncodingRequest(CommandRequestChannelParam(channel))
        )
        if len(results) != 1 or not isinstance(results[0], GetEncodingResponse):
            return None

        return results[0].value.info
