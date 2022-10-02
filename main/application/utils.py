from enum import Enum
from typing import Any

from fastapi.security import OAuth2PasswordBearer


class AutoName(Enum):
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
