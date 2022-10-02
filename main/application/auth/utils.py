import datetime
from datetime import timedelta

from main.application.auth import PackerInterface


def create_access_token(data: dict, packer: PackerInterface, expires_delta: timedelta | None = None) -> str:
    current_date = datetime.datetime.now(tz=datetime.timezone.utc)
    expire = current_date + expires_delta if expires_delta is not None else current_date + packer.default_ttl
    return packer.pack(data, expire=expire)
