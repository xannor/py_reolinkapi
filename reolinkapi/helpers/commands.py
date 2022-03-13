""""Command helpers"""
from __future__ import annotations

from typing import Mapping, TypeVar
from typing_extensions import TypeGuard

from ..typings.commands import (
    COMMAND_REQUEST_PARAM_LITERAL,
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

T = TypeVar("T")


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
        return key in request["param"] and isinstance(
            request["param"][key], __class_or_tuple
        )

    return _typeguard


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
        return key in response["value"] and isinstance(
            response["value"][key], __class_or_tuple
        )

    return _typeguard


isresponse = create_value_has_key("rspCode", CommandResponseCodeValue, int)
