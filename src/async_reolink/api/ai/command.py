"""AI Commands"""

from typing import Mapping, MutableMapping, Protocol, TypeAlias
from ..connection.typing import ChannelValue
from .typing import AITypes, AlarmState, Config


class GetAiStateRequest(ChannelValue, Protocol):
    """Get AI State"""


AiStateResponseState: TypeAlias = Mapping[AITypes, AlarmState]


class GetAiStateResponse(ChannelValue, Protocol):
    """Get AI State Response"""

    state: AiStateResponseState


class GetAiConfigRequest(ChannelValue, Protocol):
    """Get AI Configuration"""


class GetAiConfigResponse(ChannelValue, Protocol):
    """Get AI Configuration Response"""

    config: Config


class SetAiConfigRequest(ChannelValue, Protocol):
    """Set AI Configuration"""

    detect_type: MutableMapping[AITypes, bool]
    ai_track: bool
    track_type: MutableMapping[AITypes, bool]
