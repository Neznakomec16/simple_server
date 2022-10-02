from datetime import datetime, timedelta, timezone
from typing import Any, Mapping

from jwt import ExpiredSignatureError, PyJWTError, decode, encode

from main.application.auth.exceptions import ExpiredTokenError, JWTPackerError
from main.application.auth.packer_interface import PackerInterface


class JWTPacker(PackerInterface):
    def __init__(self, secret_key: str, *, default_ttl: timedelta, algorythm: str = "HS256"):
        self._default_ttl = default_ttl
        self._secret_key = secret_key
        self._algorythm = algorythm

    @property
    def default_ttl(self):
        return self._default_ttl

    def pack(self, payload: Mapping[str, Any], *, expire: datetime | None = None) -> str:
        session = {"exp": (expire or (datetime.now(tz=timezone.utc) + self._default_ttl)).timestamp()}
        session.update(payload)
        session.update({"iat": datetime.now(tz=timezone.utc)})
        return encode(session, self._secret_key, algorithm=self._algorythm)

    def unpack(self, token: str) -> Mapping[str, Any]:
        try:
            return decode(token, self._secret_key, algorithms=[self._algorythm], options={"require": ["iat", "exp"]})
        except ExpiredSignatureError:
            raise ExpiredTokenError
        except PyJWTError:
            raise JWTPackerError
