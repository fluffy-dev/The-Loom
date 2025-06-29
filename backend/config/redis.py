from pydantic import Field
from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    """
    Configuration for the Redis client, read from environment variables.
    """
    REDIS_HOST: str = Field("localhost", alias="REDIS_HOST")
    REDIS_PORT: int = Field(6379, alias="REDIS_PORT")

redis_config = RedisConfig()