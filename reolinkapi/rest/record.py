"""Record command"""

import random
import string
from typing import Final

from . import connection

from ..typings.commands import (
    CommandRequestWithParam,
    CommandChannelParameter,
    CommandRequestTypes,
)


_rnd = random.SystemRandom()
_RND_SET = string.printable


class SnapshotRequestParameter(CommandChannelParameter):
    """Snapshot Command Request Parameter"""

    rs: str


SNAPSHOT_COMMAND: Final = "Snap"


class Record:
    """Record Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        other: any = self
        if isinstance(other, connection.Connection) and not hasattr(
            self, "_execute_request"
        ):
            self._execute_request = other._execute_request

    async def get_snap(self, channel: int = 0):
        """get snapshot"""

        seed = "".join(_rnd.choice(_RND_SET) for _ in range(16))
        response = await self._execute_request(
            CommandRequestWithParam(
                cmd=SNAPSHOT_COMMAND,
                action=CommandRequestTypes.VALUE_ONLY,
                param=SnapshotRequestParameter(channel=channel, rs=seed),
            ),
            use_get=True,  # Duo repeats channel 0 with a post snap request
        )
        if response is None:
            return None

        try:
            return await response.read()
        finally:
            response.close()
