"""Encoding helpers"""

from typing import Final, Iterable, TypedDict


from . import commands as commandHelpers
from ..typings.commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)
from ..typings.encoding import EncodingInfo


class GetEncodingResponseValue(TypedDict):
    """Get Encoding Response Value"""

    Enc: EncodingInfo


GET_ENCODING_COMMAND: Final = "GetEnc"

_isEncoding = commandHelpers.create_value_has_key("Enc", GetEncodingResponseValue)


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


def get_encoding_responses(responses: Iterable[CommandResponse]):
    """Get Encoding Responses"""

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
