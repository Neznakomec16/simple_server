from fastapi import Depends, HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from main.application.auth import JWTPackerError, PackerInterface
from main.application.context import jwt_context, user_repository_context
from main.application.repositories import UserRecord, UserRepositoryInterface
from main.application.routes.users.exceptions import (
    TokenExpiredError,
    UserDoesNotExistsHTTPError,
)
from main.application.utils import oauth2_scheme


class TokenData(BaseModel):
    username: str


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    packer: PackerInterface = jwt_context.get(request)
    try:
        payload = packer.unpack(token)
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
    except JWTPackerError:
        raise TokenExpiredError
    user_repo: UserRepositoryInterface = user_repository_context.get(request)
    user = await user_repo.get_user_by_username(token_data.username, raise_if_not_exists=False)
    if user is None:
        raise UserDoesNotExistsHTTPError()
    return user


async def get_current_active_user(current_user: UserRecord = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
