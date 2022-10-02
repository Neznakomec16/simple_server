from fastapi import APIRouter

from main.application.repositories import UserRecord
from .register import register
from .token import token, TokenHandlerResponse

auth_router = APIRouter(prefix="/auth")
auth_router.add_api_route("/token", token, response_model=TokenHandlerResponse, methods=["POST"])
auth_router.add_api_route("/register", register, response_model=UserRecord, methods=["POST"])
