from pydantic import Field
from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    """
    Configuration for authentication, read from environment variables or defaults.
    """
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = Field("HS256", alias="HASH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, alias="REFRESH_TOKEN_EXPIRE_DAYS")

auth_config = AuthConfig()