""" Encoding Commands """
from __future__ import annotations
from typing import Iterable, TypedDict

from .typings.commands import (
    CommandChannelParameter,
    CommandRequest,
    CommandRequestTypes,
    CommandResponse,
    filter_command_responses,
)

from .typings.encoding import EncodingInfo

from .connection import Connection


class GetEncodingResponseValue(TypedDict):
    """Get Encoding Response Value"""

    Enc: EncodingInfo


def _cast_encoding_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetEncodingResponseValue = response["value"]
        return value["Enc"]

    return map(_cast, responses)


GET_ENCODING_COMMAND = "GetEnc"


class Encoding:
    """Encoding Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute

    @staticmethod
    def create_get_encoding(
        channel: int = 0,
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create Encoding Request"""
        return CommandRequest(
            cmd=GET_ENCODING_COMMAND,
            action=_type,
            param=CommandChannelParameter(channel=channel),
        )

    @staticmethod
    def get_encoding_responses(responses: Iterable[CommandResponse]):
        """Get Encoding Responses"""

        return _cast_encoding_response_value(
            filter_command_responses(GET_ENCODING_COMMAND, responses)
        )

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        devinfo = next(
            _cast_encoding_response_value(
                filter_command_responses(
                    GET_ENCODING_COMMAND,
                    await self._execute(Encoding.create_get_encoding(channel)),
                )
            ),
            None,
        )
        return devinfo
