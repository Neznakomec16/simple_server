from pydantic import BaseModel, Field, EmailStr, SecretStr
from starlette.requests import Request
from passlib.hash import bcrypt

from main.application.context import user_repository_context
from main.application.repositories import UserRecord, UserRepositoryInterface
from main.application.routes.auth.exceptions import UserAlreadyExistsError


class CreateUserInfo(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr = Field(..., min_length=10, max_length=128)


async def register(request: Request, *, form_data: CreateUserInfo) -> UserRecord:
    user_repo: UserRepositoryInterface = user_repository_context.get(request)
    if await user_repo.get_user_by_email_or_username(form_data.username, form_data.email, False):
        raise UserAlreadyExistsError(
            400, detail=f"User with username {form_data.username} or email {form_data.email} already exists"
        )
    form_data.password = bcrypt.hash(form_data.password.get_secret_value())
    return await user_repo.create_user(**form_data.dict())
