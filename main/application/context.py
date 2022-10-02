from starlette.requests import Request

from main.application.app_ext import ConfiguredFastAPI


class Context:
    def __init__(self, key: str):
        self._key = key

    def register(self, instance: ConfiguredFastAPI, value: any):
        instance.config[self._key] = value

    def get(self, instance: ConfiguredFastAPI | Request):
        return (
            instance.config.get(self._key)
            if isinstance(instance, ConfiguredFastAPI)
            else instance.app.config.get(self._key)
        )


config_context = Context("config_context")
postgres_context = Context("postgres_context")
redis_context = Context("redis_context")
jwt_context = Context("jwt_context")

# Repositories
user_repository_context = Context("user_repository_context")
