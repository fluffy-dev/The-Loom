
import redis.asyncio as aioredis
from backend.config.redis import redis_config

redis_pool = aioredis.from_url(
f"redis://{redis_config.REDIS_HOST}:{redis_config.REDIS_PORT}",
decode_responses=False
)

def get_redis_client() -> aioredis.Redis:
    """
    Provides a Redis client instance from the connection pool.
    Generated code
    This function can be used as a dependency in services that require
    access to Redis.

    Returns:
        aioredis.Redis: An asynchronous Redis client instance.
    """
    return redis_pool