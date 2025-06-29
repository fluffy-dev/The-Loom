from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import exc

from app.config.database.settings import settings


class DatabaseHelper:
    """
    A class to manage database connections and sessions using SQLAlchemy.

    This class provides an asynchronous engine and session factory for
    interacting with the database.
    """

    def __init__(self, url: str, echo: bool = False):
        """
        Initializes the DatabaseHelper.

        Args:
            url (str): The database connection URL.
            echo (bool): If True, the engine will log all statements.
        """
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self):
        """
        Generator function to provide a database session for FastAPI dependencies.

        This is the primary method to be used with `Depends`. It ensures the
        session is properly closed and rolled back on error.

        Yields:
            AsyncSession: An asynchronous database session.

        Raises:
            exc.SQLAlchemyError: If a database error occurs during the session.
        """
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


db_helper = DatabaseHelper(settings.database_url, settings.db_echo_log)