"""Alarm Commands"""

from __future__ import annotations

from . import connection

from ..helpers import alarm as alarmHelpers


class Alarm:
    """Alarm Mixin"""

    async def get_md_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(alarmHelpers.create_get_md_state(channel))
        else:
            return None

        state = next(alarmHelpers.get_md_state_responses(responses), None)
        return state
