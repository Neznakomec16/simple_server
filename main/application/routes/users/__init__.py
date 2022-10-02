from fastapi import APIRouter

from main.application.repositories import UserRecord
from main.application.routes.users.me import read_users_me

users_router = APIRouter(prefix="/users")
users_router.add_api_route("/me", read_users_me, methods=["GET"], response_model=UserRecord)
