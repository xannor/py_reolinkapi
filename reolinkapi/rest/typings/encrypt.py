"""Encryption Typings"""


from typing import TypedDict


class DigestInfo(TypedDict):
    """Encryption Digest"""

    Cnonce: str
    Method: str
    Nc: str
    Nonce: str
    Qop: str
    Realm: str
    Response: str
    Uri: str
    UserName: str
