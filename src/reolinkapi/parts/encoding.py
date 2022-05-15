""" Encoding Commands """

from __future__ import annotations

from . import connection

from ..helpers import encoding as encodingHelpers


class Encoding:
    """Encoding Mixin"""

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(
                encodingHelpers.create_get_encoding(channel)
            )
        else:
            return None

        return next(encodingHelpers.get_encoding_responses(responses), None)
