"""AI Commands"""

from typing import Mapping, MutableMapping, Protocol
from ..connection.typing import ChannelValue
from .typing import AITypes, AlarmState, Config


class GetAiStateRequest(ChannelValue, Protocol):
    """Get AI State"""


class GetAiStateResponse(ChannelValue, Protocol):
    """Get AI State Response"""

    state: Mapping[AITypes, AlarmState]


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
