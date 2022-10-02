from fastapi import FastAPI

from main.application.app_ext import ConfiguredFastAPI
from main.application.config import Config
from main.application.context import config_context
from main.application.routes import configure_routes
from main.application.startup_signals import postgres_signal, redis_signal, repositories_signal, packer_signal


def create_app(config: Config) -> FastAPI:
    app = ConfiguredFastAPI()
    config_context.register(app, config)
    app.signals.extend([postgres_signal(app), redis_signal(app), repositories_signal(app), packer_signal(app)])
    configure_routes(app)

    return app
