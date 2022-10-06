from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from pydantic import BaseModel
from starlette.requests import Request

from main.application.auth import PackerInterface
from main.application.auth.utils import create_access_token
from main.application.context import jwt_context, user_repository_context
from main.application.repositories import UserRepositoryInterface


class IncorrectUsernameOrPasswordError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Incorrect username or password")


class TokenHandlerResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


async def token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user_repo: UserRepositoryInterface = user_repository_context.get(request)
    user = await user_repo.get_user_by_username(form_data.username, raise_if_not_exists=False)
    if user is None:
        raise IncorrectUsernameOrPasswordError()
    if not bcrypt.verify(form_data.password, user.password):
        raise IncorrectUsernameOrPasswordError()
    packer: PackerInterface = jwt_context.get(request)
    await user_repo.update_last_login(user.username)
    return TokenHandlerResponse(access_token=create_access_token(data={"sub": user.username}, packer=packer))
