from fastapi import FastAPI

from main.application.routes.auth import auth_router
from main.application.routes.services import services_router
from main.application.routes.users import users_router


def configure_routes(app: FastAPI):
    app.include_router(services_router)
    app.include_router(auth_router)
    app.include_router(users_router)
