"""Record command"""

import random
import string
from typing import TypedDict

from .connection import Connection

from .typings.commands import (
    CommandRequest,
    CommandChannelParameter,
    CommandRequestTypes,
)


_rnd = random.SystemRandom()
_RND_SET = string.printable


class SnapshotRequestParameter(CommandChannelParameter):
    """Snapshot Command Request Parameter"""

    rs: str


SNAPSHOT_COMMAND = "Snap"


class Record:
    """Record Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self, Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute
            self._execute_response = self._execute_response

    async def get_snap(self, channel: int = 0):
        """get snapshot"""

        seed = "".join(_rnd.choice(_RND_SET) for _ in range(16))
        response = await self._execute_response(
            CommandRequest(
                cmd=SNAPSHOT_COMMAND,
                action=CommandRequestTypes.VALUE_ONLY,
                param=SnapshotRequestParameter(channel=channel, rs=seed),
            )
        )
        if response is None:
            return None

        try:
            return await response.read()
        finally:
            response.close()
