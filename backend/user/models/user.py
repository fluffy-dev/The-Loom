from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base


class UserModel(Base):
    """
    SQLAlchemy model for users.
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(30))
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))

    owned_rooms: Mapped[List["RoomModel"]] = relationship(back_populates="owner")
    participated_rooms: Mapped[List["RoomParticipantModel"]] = relationship(back_populates="user")