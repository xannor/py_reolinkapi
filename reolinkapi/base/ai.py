"""AI Commands"""
from __future__ import annotations

from ..helpers import ai as aiHelpers

from . import connection


class AI:
    """AI Mixin"""

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(aiHelpers.create_get_ai_state(channel))
        else:
            return None

        state = next(aiHelpers.get_ai_state_responses(responses), None)
        return state

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(aiHelpers.create_get_ai_config(channel))
        else:
            return None

        config = next(aiHelpers.get_ai_config_responses(responses), None)
        return config
