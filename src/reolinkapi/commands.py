"""Commands"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Final, Generic, TypeGuard, TypeVar, TypedDict
from typing_extensions import Literal, NotRequired

from pyparsing import Iterable, Mapping


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
    action: int

_T = TypeVar("_T")

@dataclass
class CommandRequestWithParam(CommandRequest, Generic[_T]):
    """Command Request"""

    param: _T


CommandResponseType = dict[str,any]

class CommandResponse(TypedDict):
    """Command Response"""

    cmd: str
    code: int


COMMAND: Final = "cmd"

# this should be generic but they are not supported yet
class CommandResponseValue(CommandResponse):
    """Command Response Value"""

    value: CommandResponseType
    initial: NotRequired[CommandResponseType]
    range: NotRequired[CommandResponseType]


COMMAND_RESPONSE_VALUE: Final = "value"
#COMMAND_RESPONSE_VALUE_LITERAL: Final = Literal["value"]


class CommandResponseCodeValue(TypedDict):
    """Command Response Code Value"""

    rspCode: int


COMMAND_RESPONSE_CODE: Final = "rspCode"


class ErrorCode(TypedDict):
    """Error Code"""

    rspCode: int
    detail: str


class CommandResponseErrorValue(CommandResponse):
    """Command Response Error Value"""

    error: ErrorCode


COMMAND_RESPONSE_ERROR: Final = "error"

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
    key: str, __type: type[_T], __class_or_tuple: type | tuple = dict
):
    """Create Value Typeguard"""

    def _typeguard(
        response: CommandResponseValue,
    ) -> TypeGuard[Mapping[Literal['value'], _T]]:
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
