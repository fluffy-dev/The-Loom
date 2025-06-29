from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database.base import Base


class UserModel(Base):
    """
    SQLAlchemy model representing a user in the database.
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)