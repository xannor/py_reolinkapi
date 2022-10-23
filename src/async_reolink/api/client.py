""" Reolink Client """

from abc import ABC

from .ai.mixin import AI

from .alarm.mixin import Alarm

from .connection.mixin import Connection

from .encoding.mixin import Encoding

from .led.mixin import LED

from .network.mixin import Network

from .ptz.mixin import PTZ

from .record.mixin import Record

from .security.mixin import Security

from .system.mixin import System

from .video.mixin import Video

from .__version__ import __version__


class Client(
    Connection,
    Security,
    System,
    Network,
    Video,
    Encoding,
    Record,
    Alarm,
    AI,
    LED,
    PTZ,
    ABC,
):
    """API Client"""
