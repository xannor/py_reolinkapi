""""Command helpers"""
from __future__ import annotations

from typing import Iterable, Mapping, TypeVar
from typing_extensions import TypeGuard

from ..typings.commands import (
    COMMAND,
    COMMAND_REQUEST_PARAM_LITERAL,
    COMMAND_RESPONSE_CODE,
    COMMAND_RESPONSE_VALUE_LITERAL,
    CommandRequest,
    CommandRequestWithParam,
    COMMAND_REQUEST_PARAM,
    CommandResponse,
    CommandResponseCodeValue,
    CommandResponseValue,
    COMMAND_RESPONSE_VALUE,
    CommandResponseErrorValue,
    COMMAND_RESPONSE_ERROR,
)

T = TypeVar("T")  # pylint: disable=invalid-name


def isparam(request: CommandRequest) -> TypeGuard[CommandRequestWithParam]:
    """is a command reqiest with parameters"""

    return COMMAND_REQUEST_PARAM in request and isinstance(
        request[COMMAND_REQUEST_PARAM], dict
    )


def create_param_has_key(
    key: str, __type: type[T], __class_or_tuple: type | tuple = dict
):
    """Create Param Typeguard"""

    def _typeguard(
        request: CommandRequestWithParam,
    ) -> TypeGuard[Mapping[COMMAND_REQUEST_PARAM_LITERAL, T]]:
        return key in request[COMMAND_REQUEST_PARAM] and isinstance(
            request[COMMAND_REQUEST_PARAM][key], __class_or_tuple
        )

    return _typeguard


def create_is_command(command: str):
    """Create Command Typeguard"""

    def _filter(response: CommandResponse):
        return response[COMMAND] == command

    return _filter


def isvalue(response: CommandResponse) -> TypeGuard[CommandResponseValue]:
    """is a command value response"""

    return COMMAND_RESPONSE_VALUE in response and isinstance(
        response[COMMAND_RESPONSE_VALUE], dict
    )


def iserror(response: CommandResponse) -> TypeGuard[CommandResponseErrorValue]:
    """is a command error response"""

    return COMMAND_RESPONSE_ERROR in response and isinstance(
        response[COMMAND_RESPONSE_ERROR], dict
    )


def create_value_has_key(
    key: str, __type: type[T], __class_or_tuple: type | tuple = dict
):
    """Create Value Typeguard"""

    def _typeguard(
        response: CommandResponseValue,
    ) -> TypeGuard[Mapping[COMMAND_RESPONSE_VALUE_LITERAL, T]]:
        return key in response[COMMAND_RESPONSE_VALUE] and isinstance(
            response[COMMAND_RESPONSE_VALUE][key], __class_or_tuple
        )

    return _typeguard


isresponseCode = create_value_has_key(
    COMMAND_RESPONSE_CODE, CommandResponseCodeValue, int
)


def get_response_codes(responses: Iterable[CommandResponse]):
    """Get Response Codes"""

    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE][COMMAND_RESPONSE_CODE],
        filter(isresponseCode, filter(isvalue, responses)),
    )
