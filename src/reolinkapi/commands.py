"""Commands"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Final, Generic, Type, TypeVar, TypedDict, Mapping, overload
from typing_extensions import Literal, NotRequired, TypeGuard


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

    @classmethod
    def is_response(
        cls,
        value: any,
        *,
        command: str | None = None
    ) -> TypeGuard[CommandResponseType]:
        """value is Response"""
        if not isinstance(value, dict) or not COMMAND in value:
            return False
        if command is None:
            return True
        return value[COMMAND] == command

    @classmethod
    def _is_value(cls, value: CommandResponseType) -> TypeGuard[CommandResponseValueType]:
        return (
            COMMAND_RESPONSE_VALUE in value
            and isinstance(value[COMMAND_RESPONSE_VALUE], dict)
        )

    @classmethod
    def _is_typed_value(cls, value: CommandResponseType, key: str, __type: Type[_T]) -> TypeGuard[Mapping[COMMAND_RESPONSE_VALUE_LITERAL, _T]]:
        return (
            cls._is_value(value)
            and key in value[COMMAND_RESPONSE_VALUE]
        )

    @classmethod
    def is_value(
        cls,
        value: any,
        *,
        command: str | None = None,
        **_
    ) -> TypeGuard[CommandResponseValueType]:
        """value is Response Value"""
        return (
            cls.is_response(value, command=command)
            and cls._is_value(value)
        )

    @overload
    @classmethod
    def _get_value(
        cls, value: Mapping[COMMAND_RESPONSE_VALUE_LITERAL, _T]) -> _T: ...

    @overload
    @classmethod
    def _get_value(cls, value: CommandResponseValueType) -> dict: ...

    @classmethod
    def _get_value(cls, value: dict):
        return value[COMMAND_RESPONSE_VALUE]

    @overload
    @classmethod
    def get_value(cls, value: CommandResponseValueType) -> dict: ...

    @overload
    @classmethod
    def get_value(
        cls, value: Mapping[COMMAND_RESPONSE_VALUE_LITERAL, _T]) -> _T: ...

    @classmethod
    def get_value(
        cls,
        value: any,
        *,
        command: str | None = None
    ):
        """get Response Value"""
        if cls.is_value(value, command=command):
            return value[COMMAND_RESPONSE_VALUE]
        return None

    @classmethod
    def is_error(
        cls,
        value: any,
        *,
        command: str | None = None
    ) -> TypeGuard[CommandResponseErrorValueType]:
        """value is Response Error"""
        return (
            cls.is_response(value, command=command)
            and COMMAND_RESPONSE_ERROR in value
            and isinstance(value[COMMAND_RESPONSE_ERROR], dict)
        )

    @classmethod
    def get_error(
        cls,
        value: any,
        *,
        command: str | None = None
    ):
        """get error code"""
        if cls.is_error(value, command=command):
            return value[COMMAND_RESPONSE_ERROR]
        return None

    @classmethod
    def _is_response_code(cls, value: CommandResponseType) -> TypeGuard[Mapping[COMMAND_RESPONSE_VALUE_LITERAL, CommandResponseCodeValueType]]:
        return cls._is_typed_value(value, COMMAND_RESPONSE_CODE, CommandResponseCodeValueType)

    @classmethod
    def is_response_code(
        cls,
        value: any,
        *,
        command: str | None = None
    ) -> TypeGuard[Mapping[COMMAND_RESPONSE_VALUE_LITERAL, CommandResponseCodeValueType]]:
        """value is Response Code"""
        return (
            cls.is_response(value, command=command)
            and cls._is_response_code(value)
        )

    @classmethod
    def _get_response_code(cls, value: Mapping[COMMAND_RESPONSE_VALUE_LITERAL, CommandResponseCodeValueType]):
        return value[COMMAND_RESPONSE_VALUE][COMMAND_RESPONSE_CODE]

    @overload
    @classmethod
    def get_response_code(
        cls,
        value: Mapping[COMMAND_RESPONSE_VALUE_LITERAL,
                       CommandResponseCodeValueType]
    ) -> int: ...

    @classmethod
    def get_response_code(
        cls,
        value: any,
        *,
        command: str | None = None
    ):
        """get response code"""
        if cls.is_response_code(value, command=command):
            return cls._get_response_code(value)
        return None


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
COMMAND_RESPONSE_VALUE_LITERAL: Final = Literal["value"]


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
