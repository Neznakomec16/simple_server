from aioredis import ConnectionError


async def check_postgres(pg_connect) -> bool:
    try:
        return (await pg_connect.fetchval("SELECT 1;")) == 1
    except OSError:
        return False


async def check_redis(redis) -> bool:
    test_key, test_value = "test_key", b"test_value"
    try:
        await redis.set(test_key, test_value)
        redis_status = (await redis.get(test_key)) == test_value
        await redis.delete(test_key)
    except ConnectionError:
        return False
    return redis_status
