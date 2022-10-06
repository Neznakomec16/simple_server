import logging

import aioredis
import asyncpg
from aioredis import Redis

from main.application.app_ext import ConfiguredFastAPI
from main.application.auth.jwt import JWTPacker
from main.application.config import Config
from main.application.context import (
    config_context,
    jwt_context,
    postgres_context,
    redis_context,
    user_repository_context,
)
from main.application.repositories import PostgresUserRepository

logger = logging.getLogger(__name__)


async def postgres_signal(app: ConfiguredFastAPI):
    config: Config = config_context.get(app)
    conn = await asyncpg.create_pool(
        config.postgres_config.dsn,
        # min_size=config.postgres_config
    )
    logger.info(f"Setting up postgres connection pool")
    async with conn.acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchval("SELECT 1;")
            assert result == 1
    postgres_context.register(app, conn)
    logger.info(f"Postgres connection pool created")
    yield


async def redis_signal(app: ConfiguredFastAPI):
    config: Config = config_context.get(app)
    logger.info(f"Setting up redis connection")
    redis: Redis = await aioredis.from_url(config.redis_config.dsn)
    test_key, test_value = "test_key", b"test_value"
    await redis.set(test_key, test_value)
    value = await redis.get(test_key)
    assert value == test_value
    await redis.delete(test_key)
    logger.info(f"Redis connection created")
    redis_context.register(app, redis)
    yield


async def repositories_signal(app: ConfiguredFastAPI):
    """
    Function to initialize that are specified
    at auth_server.application.repositories
    """
    pg = postgres_context.get(app)
    pg_user_repo = PostgresUserRepository(pg)
    user_repository_context.register(app, pg_user_repo)
    yield


async def packer_signal(app: ConfiguredFastAPI):
    config: Config = config_context.get(app)
    packer = JWTPacker(config.jwt_config.secret_key, default_ttl=config.jwt_config.default_ttl)
    jwt_context.register(app, packer)
    yield
