from datetime import datetime
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models with common columns.

    This abstract base class provides each inheriting model with an integer
    primary key (`id`), a creation timestamp (`created_at`), and an
    update timestamp (`updated_at`). The timestamps are managed automatically
    by the database.

    Attributes:
        id (Mapped[int]): The primary key for the table, auto-incrementing.
        created_at (Mapped[datetime]): Timestamp of when the record was created.
        updated_at (Mapped[datetime]): Timestamp of the last update to the record.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )