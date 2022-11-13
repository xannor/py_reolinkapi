"""LED Commands"""

from typing import Protocol

from ..connection.typing import ChannelValue
from .typing import LightStates, WhiteLedInfo


class GetIrLightsRequest(ChannelValue, Protocol):
    """Get IR Lights"""


class GetIrLightsResponse(ChannelValue, Protocol):
    """Get IR Lights Response"""

    state: LightStates


class SetIrLightsRequest(ChannelValue, Protocol):
    """Set Ir Lights"""

    state: LightStates


class GetPowerLedRequest(ChannelValue, Protocol):
    """Get Power Led"""


class GetPowerLedResponse(ChannelValue, Protocol):
    """Get Power Led Response"""

    state: LightStates


class SetPowerLedRequest(ChannelValue, Protocol):
    """Set Power Led"""

    state: LightStates


class GetWhiteLedRequest(ChannelValue, Protocol):
    """Get White Led"""


class GetWhiteLedResponse(ChannelValue, Protocol):
    """Get White Led Response"""

    info: WhiteLedInfo


class SetWhiteLedRequest(ChannelValue, Protocol):
    """Set White Led"""

    info: WhiteLedInfo
