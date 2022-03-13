""" Rest API client """

from .led import LED
from .network import Network
from .connection import Connection, SessionFactory
from .security import Security
from .encrypt import Encrypt
from .system import System
from .video import Video
from .encoding import Encoding
from .record import Record
from .alarm import Alarm
from .ai import AI


class Client(
    Connection,
    Security,
    Encrypt,
    System,
    Network,
    Video,
    Encoding,
    Record,
    Alarm,
    AI,
    LED,
):
    """Rest API Client"""

    def __init__(self, session_factory: SessionFactory = None) -> None:
        """not usless"""
        super().__init__(session_factory=session_factory)
