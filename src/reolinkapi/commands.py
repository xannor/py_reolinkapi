"""Commands"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import (
    AsyncIterable,
    Callable,
    Final,
    Generic,
    Iterable,
    Optional,
    Protocol,
    Type,
    TypeVar,
    TypedDict,
    Mapping,
    Literal,
    overload,
)
from typing_extensions import NotRequired, TypeGuard

from .errors import ErrorCodes, ReolinkResponseError


_T = TypeVar("_T")
_K = TypeVar("_K")


class CommandRequestTypes(IntEnum):
    """Command Action Types"""

    VALUE_ONLY: Final = 0
    DETAILED: Final = 1


COMMAND_REQUEST_TYPE: Final = "action"


@dataclass
class CommandChannelParameter:
    """Command Request Channel Parameter"""

    channel: int


@dataclass
class CommandRequest:
    """Command Request"""

    cmd: str
    action: CommandRequestTypes

    @staticmethod
    def _is_response(
        value: any, command: str | None = None
    ) -> TypeGuard[CommandResponseType]:
        return (
            isinstance(value, dict)
            and COMMAND in value
            and (command is None or value[COMMAND] == command)
        )

    @classmethod
    def is_response(
        cls, value: any, *, command: str | None = None, **_
    ) -> TypeGuard[CommandResponseType]:
        """value is Response"""
        return CommandRequest._is_response(value, command)

    @staticmethod
    def _is_value(value: CommandResponseType) -> TypeGuard[CommandResponseValueType]:
        return COMMAND_RESPONSE_VALUE in value and isinstance(
            value[COMMAND_RESPONSE_VALUE], dict
        )

    @staticmethod
    def _is_typed_value(
        value: CommandResponseType, key: str, __type: Type[_T]
    ) -> TypeGuard[CommandResponseValue[_T]]:
        return CommandRequest._is_value(value) and key in value[COMMAND_RESPONSE_VALUE]

    @staticmethod
    def is_value(
        value: any, *, command: str | None = None, **_
    ) -> TypeGuard[CommandResponseValueType]:
        """value is Response Value"""
        return CommandRequest._is_response(
            value, command=command
        ) and CommandRequest._is_value(value)

    @overload
    @staticmethod
    def _get_value(value: CommandResponseValue[_T]) -> _T:
        ...

    @overload
    @staticmethod
    def _get_value(value: CommandResponseValueType) -> dict:
        ...

    @staticmethod
    def _get_value(value: dict):
        return value[COMMAND_RESPONSE_VALUE]

    @overload
    @classmethod
    def get_value(cls, value: CommandResponseValue[_T]) -> _T:
        ...

    @overload
    @classmethod
    def get_value(cls, value: CommandResponseValueType) -> dict:
        ...

    @classmethod
    def get_value(cls, value: CommandResponseValueType):
        """get Response Value"""
        return value[COMMAND_RESPONSE_VALUE]

    @staticmethod
    def _is_error(
        value: CommandResponseType,
    ) -> TypeGuard[CommandResponseErrorValueType]:
        return COMMAND_RESPONSE_ERROR in value and isinstance(
            value[COMMAND_RESPONSE_ERROR], dict
        )

    @classmethod
    def is_error(
        cls, value: CommandResponseType
    ) -> TypeGuard[CommandResponseErrorValueType]:
        """value is Response Error"""
        return CommandRequest._is_error(value)

    @staticmethod
    def _get_error(value: CommandResponseErrorValueType):
        return value[COMMAND_RESPONSE_ERROR]

    @classmethod
    def get_error(cls, value: CommandResponseErrorValueType):
        """get error code"""
        return CommandRequest._get_error(value)

    @staticmethod
    def _is_response_code(
        value: CommandResponseType,
    ) -> TypeGuard[CommandResponseValue[CommandResponseCodeValueType]]:
        return CommandRequest._is_typed_value(
            value, COMMAND_RESPONSE_CODE, CommandResponseCodeValueType
        )

    @classmethod
    def is_response_code(
        cls, value: CommandResponseType
    ) -> TypeGuard[CommandResponseValue[CommandResponseCodeValueType]]:
        """value is Response Code"""
        return CommandRequest._is_response_code(value)

    @staticmethod
    def _get_response_code(value: CommandResponseValue[CommandResponseCodeValueType]):
        return value[COMMAND_RESPONSE_VALUE][COMMAND_RESPONSE_CODE]

    @classmethod
    def get_response_code(
        cls, value: CommandResponseValue[CommandResponseCodeValueType]
    ):
        """get response code"""
        return CommandRequest._get_response_code(value)


@dataclass
class CommandRequestWithParam(CommandRequest, Generic[_T]):
    """Command Request"""

    param: _T


class CommandResponseType(TypedDict):
    """Command Response"""

    cmd: str
    code: int


COMMAND: Final = "cmd"

# this should be generic but they are not supported yet


class CommandResponseValueType(CommandResponseType):
    """Command Response Value"""

    value: dict
    initial: NotRequired[dict]
    range: NotRequired[dict]


COMMAND_RESPONSE_VALUE: Final = "value"
CommandResponseValue = Mapping[Literal["value"], _T]
CommandResponseInitial = Mapping[Literal["initial"], _T]
CommandResponseRange = Mapping[Literal["range"], _T]


class CommandResponseChannelValueType(TypedDict):
    """Command Response Channel Value"""

    channel: int


class CommandResponseCodeValueType(TypedDict):
    """Command Response Code Value"""

    rspCode: int


COMMAND_RESPONSE_CODE: Final = "rspCode"


class ErrorCodeType(CommandResponseCodeValueType):
    """Error Code"""

    detail: str


class CommandResponseErrorValueType(CommandResponseType):
    """Command Response Error Value"""

    error: ErrorCodeType


COMMAND_RESPONSE_ERROR: Final = "error"


class TrapCallback(Protocol):
    """Error Trap"""

    def __call__(self, code: ErrorCodes, details: str | None = None) -> any:
        ...


def _raise_response_error(code: ErrorCodes, details: str | None = None) -> bool:
    raise ReolinkResponseError(code=code, details=details)


def trap_errors(
    responses: Iterable[CommandResponseType | bytes],
    *,
    __trap: TrapCallback | None = None,
):
    """Trap response errors"""
    for response in responses:
        if isinstance(response, (bytearray, bytes)):
            code = ErrorCodes.PROTOCOL_ERROR
            details = "Expected CommandResponses got bytes"
            if not (__trap or __trap(code, details)):
                _raise_response_error(code, details)
            continue
        if CommandRequest.is_error(response):
            error = response["error"]
            code = ErrorCodes(error["rspCode"])
            if not __trap(code, error["detail"]):
                _raise_response_error(code, error["detail"])
            continue
        yield response


async def async_trap_errors(
    responses: AsyncIterable[CommandResponseType | bytes],
    *,
    __trap: TrapCallback | None = None,
):
    """async treap response errors"""
    async for response in responses:
        if isinstance(response, (bytearray, bytes)):
            code = ErrorCodes.PROTOCOL_ERROR
            details = "Expected CommandResponses got bytes"
            if __trap:
                _r = not __trap(code, details)
            else:
                _r = True
            if _r:
                _raise_response_error(code, details)
            break
        if CommandRequest.is_error(response):
            error = response["error"]
            code = ErrorCodes(error["rspCode"])
            if __trap:
                _r = not __trap(code, error["detail"])
            else:
                _r = True
            if _r:
                _raise_response_error(code, error["detail"])
            continue
        yield response
