from fastapi import Depends

from main.application.repositories import UserRecord
from main.application.routes.users.utils import get_current_active_user


async def read_users_me(current_user: UserRecord = Depends(get_current_active_user)) -> UserRecord:
    return current_user
