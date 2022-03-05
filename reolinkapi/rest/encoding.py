""" Encoding Commands """
from __future__ import annotations
from typing import TypedDict

from .typings.commands import (
    CommandChannelParameter,
    CommandRequest,
    CommandRequestTypes,
)

from .typings.encoding import EncodingInfo

from .connection import Connection


class GetEncodingResponseValue(TypedDict):
    """Get Encoding Response Value"""

    Enc: EncodingInfo


GET_ENCODING_COMMAND = "GetEnc"


class Encoding:
    """Encoding Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        results = await self._execute(
            CommandRequest(
                cmd=GET_ENCODING_COMMAND,
                action=CommandRequestTypes.VALUE_ONLY,
                param=CommandChannelParameter(channel=channel),
            )
        )
        if (
            len(results) != 1
            or not isinstance(results[0], dict)
            or results[0]["cmd"] != GET_ENCODING_COMMAND
        ):
            return None

        value: GetEncodingResponseValue = results[0]["value"]
        return value["Enc"]
