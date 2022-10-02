from datetime import datetime

from pydantic import BaseModel, Field


class UserRecord(BaseModel):
    id: int
    username: str
    email: str
    created_dt: datetime
    last_login: datetime | None
    disabled: bool = False


class UserRecordWithPassword(UserRecord):
    password: str = Field(..., exclude=True)
