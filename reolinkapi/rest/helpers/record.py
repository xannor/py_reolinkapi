"""Record Rest Helpers"""


from ...helpers.record import SNAPSHOT_COMMAND
from ...typings.commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
)


class SnapshotRequestParameter(CommandChannelParameter):
    """Snapshot Command Request Parameter"""

    rs: str


def create_get_snapshot(
    random_seed: str,
    channel: int = 0,
    action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create Get Snapshot Request"""

    return (
        CommandRequestWithParam(
            cmd=SNAPSHOT_COMMAND,
            action=action,
            param=SnapshotRequestParameter(channel=channel, rs=random_seed),
        ),
    )
