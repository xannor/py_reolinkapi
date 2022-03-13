""" Encoding Commands """
from __future__ import annotations
from typing import Final, Iterable, TypedDict

from ..typings.commands import (
    CommandChannelParameter,
    CommandRequestWithParam,
    CommandRequestTypes,
    CommandResponse,
)

from ..typings.encoding import EncodingInfo
from ..helpers import commands as commandHelpers

from . import connection


class GetEncodingResponseValue(TypedDict):
    """Get Encoding Response Value"""

    Enc: EncodingInfo


GET_ENCODING_COMMAND: Final = "GetEnc"

_isEncoding = commandHelpers.create_value_has_key("Enc", GetEncodingResponseValue)


def _get_encoding_responses(responses: Iterable[CommandResponse]):

    return map(
        lambda response: response["value"]["Enc"],
        filter(
            _isEncoding,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_ENCODING_COMMAND, responses
                ),
            ),
        ),
    )


class Encoding:
    """Encoding Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        other: any = self
        if isinstance(other, connection.Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = other._execute

    @staticmethod
    def create_get_encoding(
        channel: int = 0,
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create Encoding Request"""
        return CommandRequestWithParam(
            cmd=GET_ENCODING_COMMAND,
            action=_type,
            param=CommandChannelParameter(channel=channel),
        )

    @staticmethod
    def get_encoding_responses(responses: Iterable[CommandResponse]):
        """Get Encoding Responses"""

        return _get_encoding_responses(responses)

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        encoding = next(
            _get_encoding_responses(
                await self._execute(Encoding.create_get_encoding(channel))
            ),
            None,
        )
        return encoding
