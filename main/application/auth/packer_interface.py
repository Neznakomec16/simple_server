from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Mapping


class PackerInterface(ABC):
    default_ttl: timedelta

    @abstractmethod
    def pack(self, payload: Mapping[str, Any], *, expire: datetime | None = None) -> str:
        ...

    @abstractmethod
    def unpack(self, token: str) -> Mapping[str, Any]:
        ...
