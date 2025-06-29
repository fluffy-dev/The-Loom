from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Database settings configuration model.

    Reads database connection details from environment variables.
    Provides a DSN property for easy connection.
    """
    db_url_scheme: str = Field("postgresql+asyncpg", alias="DB_URL_SCHEME")
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_echo_log: bool = Field(False, alias="DB_ECHO_LOG")
    db_run_auto_migrate: bool = Field(False, alias="DB_RUN_AUTO_MIGRATE")

    @property
    def database_url(self) -> str:
        """
        Constructs the full database connection URL (DSN).

        Returns:
            str: The asynchronous database connection string.
        """
        return (
            f"{self.db_url_scheme}://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()