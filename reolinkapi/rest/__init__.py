""" Rest API client """

from .network import Network
from .connection import Connection, SessionFactory
from .security import Security
from .system import System
from .video import Video
from .encoding import Encoding
from .record import Record


class Client(Connection, Security, System, Network, Video, Encoding, Record):
    """Rest API Client"""

    def __init__(self, session_factory: SessionFactory = None) -> None:
        """not usless"""
        super().__init__(session_factory=session_factory)
