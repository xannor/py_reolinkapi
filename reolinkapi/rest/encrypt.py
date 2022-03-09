"""Simple Clear Encryption Support"""
from __future__ import annotations

import base64
import hashlib
from random import SystemRandom
from typing import TypedDict, cast
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CFB

from reolinkapi.rest.typings.commands import CommandRequest, CommandRequestTypes


from . import connection, security

from .typings.encrypt import DigestInfo


class EncryptionLoginRequestParam(TypedDict):
    """Attempt to start an encrypted session"""

    Version: int


class EncrtypedLoginRequestParam(EncryptionLoginRequestParam):
    """Initial Encrypted Login Parameters"""

    Digest: DigestInfo


_IV = "bcswebapp1234567".encode("utf8")


class Encrypt:
    """Encryption Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cipher: Cipher | None = None
        other: any = self
        if isinstance(other, connection.Connection):
            if not hasattr(self, "_execute_request"):
                self._execute_request = other._execute_request
                self._process_response = other._process_response

        if isinstance(other, security.Security):
            other._logout_callbacks.append(self.__cleanup)

    def __cleanup(self):
        self.__cipher = None

    def _encrypt(self, data: str):
        if self.__cipher is None:
            return data
        context = self.__cipher.encryptor()
        edata = context.update(data.encode("utf8"))
        edata += context.finalize()
        edata = base64.b64encode(edata)
        return edata.decode("ascii")

    def _decrypt(self, data: str):
        if self.__cipher is None:
            return data

        context = self.__cipher.decryptor()
        ddata = context.update(base64.b64decode(data.encode("ascii")))
        ddata += context.finalize()
        return ddata.decode("utf8")

    def _create_cipher(self, key: str):
        self.__cipher = Cipher(AES(key.encode("ascii")), CFB(_IV))

    async def _encrypted_login(self, username: str, password: str):
        response = await self._execute_request(
            CommandRequest(
                cmd=security.LOGIN_COMMAND,
                action=CommandRequestTypes.VALUE_ONLY,
                param=EncryptionLoginRequestParam(Version=1),
            )
        )
        if response is None:
            return None
        auth = response[0].headers.get("WWW-Authenticate")
        _comma = (
            (pair.strip() for pair in auth[7:].split(","))
            if auth is not None and auth[0:7] == "Digest "
            else None
        )
        _pairs = (
            ((pair.split("=", 2)) for pair in _comma) if _comma is not None else None
        )
        _clean = (
            ((pair[0].strip(), pair[1].strip().strip('"')) for pair in _pairs)
            if _pairs is not None
            else None
        )
        auth = dict(_clean) if _clean is not None else None
        if auth is None:
            return None

        digest = cast(DigestInfo, dict())
        digest["Uri"] = response[0].url.path_qs[1:]
        response[0].close()
        digest["Realm"] = auth["realm"]
        digest["Qop"] = auth["qop"]
        digest["Nonce"] = auth["nonce"]
        digest["Nc"] = auth["nc"]
        digest["Method"] = response[0].method

        digest["Cnonce"] = SystemRandom().randbytes(24).hex()

        digest["UserName"] = username
        pwhash = hashlib.md5(
            f'{username}:{digest["Realm"]}:{password}'.encode("utf-8")
        ).hexdigest()
        _hash = hashlib.md5(
            f'{digest["Method"]}:{digest["Uri"]}'.encode("utf-8")
        ).hexdigest()
        digest["Response"] = hashlib.md5(
            f'{pwhash}:{digest["Nonce"]}:{digest["Nc"]}:{digest["Cnonce"]}:{digest["Qop"]}:{_hash}'.encode(
                "utf-8"
            )
        ).hexdigest()
        key = (
            hashlib.md5(
                f'{digest["Nonce"]}-{password}-{digest["Cnonce"]}'.encode("utf-8")
            )
            .hexdigest()[0:16]
            .upper()
        )

        response = await self._execute_request(
            CommandRequest(
                cmd=security.LOGIN_COMMAND,
                action=CommandRequestTypes.VALUE_ONLY,
                param=EncrtypedLoginRequestParam(Version=1, Digest=digest),
            )
        )
        self._create_cipher(key)
        return await self._process_response(*response)
