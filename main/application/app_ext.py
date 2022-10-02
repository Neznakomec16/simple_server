import logging
from typing import AsyncGenerator

from fastapi import FastAPI

logger = logging.getLogger(__name__)


class ConfiguredFastAPI(FastAPI):
    config = dict()
    signals: list[AsyncGenerator[None, None]] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router.on_startup.append(startup(self))
        self.router.on_shutdown.append(shutdown(self))


def startup(app: ConfiguredFastAPI):
    async def inner():
        for signal in app.signals:
            await signal.__anext__()

    return inner


def shutdown(app: ConfiguredFastAPI):
    async def inner():
        for signal in app.signals:
            try:
                await signal.__anext__()
            except StopAsyncIteration:
                logger.info(f"{signal}")

    return inner
