"""System Parts"""

from datetime import datetime
from typing import Protocol
from .capabilities import Capabilities


class System(Protocol):
    """System Part"""

    async def get_capabilities(self, username: str | None = None) -> Capabilities:
        """Get User Permisions"""

    async def get_time(self) -> datetime:
        """Get Device Time Information"""
