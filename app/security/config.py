from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    """
    Configuration for authentication settings, read from environment variables.
    """
    SECRET_KEY: str = "your_super_secret_key_that_is_long_and_random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


auth_config = AuthConfig()