from datetime import timedelta
from pathlib import Path

from pydantic import BaseSettings

from main.application.exceptions import EnvFileNotFound

BASE_DIR = Path(__file__).parent.parent.parent.resolve()


class PostgresConfig(BaseSettings):
    username: str
    password: str
    db: str
    host: str = "localhost"
    port: str = "5432"

    class Config:
        env_prefix = "POSTGRES_"

    @property
    def dsn(self) -> str:
        return f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}{"/" + self.db if self.db else ""}'

    @property
    def sqlalchemy_dsn(self) -> str:
        return f'postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}{"/" + self.db if self.db else ""}'


class RedisConfig(BaseSettings):
    db: str = "0"
    host: str = "localhost"
    port: str = "6379"

    class Config:
        env_prefix = "REDIS_"

    @property
    def dsn(self) -> str:
        return f'redis://{self.host}:{self.port}{"/" + self.db if self.db else ""}'


class JWTConfig(BaseSettings):
    secret_key: str
    default_ttl: timedelta = timedelta(minutes=60)
    algorythm: str = "HS256"

    class Config:
        env_prefix = "JWT_"


class Config(BaseSettings):
    postgres_config: PostgresConfig
    redis_config: RedisConfig
    jwt_config: JWTConfig

    @classmethod
    def get_from_env(cls):
        return cls(postgres_config=PostgresConfig(), redis_config=RedisConfig(), jwt_config=JWTConfig())

    @classmethod
    def get_from_env_file(cls, file_path: Path):
        import os

        if not file_path.exists():
            raise EnvFileNotFound(f"Config file with path {file_path.as_uri()} not found")
        with open(file_path, "r") as file:
            keys = []
            while line := file.readline():
                if line == "\n" or line.startswith("#"):
                    continue
                key, value = line.strip("\n").split("=")
                keys.append(key)
                os.environ[key] = value
            config = cls.get_from_env()
            for key in keys:
                del os.environ[key]
            return config
