"""Record command"""

import random
import string

from .helpers import record as recordHelpers

from ..base.record import Record as BaseRecord
from . import connection

_rnd = random.SystemRandom()
_RND_SET = string.printable


class Record(BaseRecord):
    """Record Mixin"""

    async def get_snap(self, channel: int = 0):
        """get snapshot"""

        if isinstance(self, connection.Connection):
            seed = "".join(_rnd.choice(_RND_SET) for _ in range(16))

            response = await self._execute_request(
                recordHelpers.create_get_snapshot(seed, channel),
                use_get=True,  # Duo repeats channel 0 with a post snap request
            )

        else:
            return None

        if response is None:
            return None

        try:
            return await response.read()
        finally:
            response.close()
