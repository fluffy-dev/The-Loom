from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base

class RoomModel(Base):
    """
    SQLAlchemy model for a collaboration room.

    Attributes:
        human_readable_id (Mapped[str]): A short, user-friendly, unique ID for the room.
        owner_id (Mapped[int]): The ID of the user who owns this room.
        owner (Mapped["UserModel"]): Relationship to the owner user.
        participants (Mapped[List["RoomParticipantModel"]]): List of all participants in the room.
        files (Mapped[List["FileMetadataModel"]]): List of all files in the room.
    """
    __tablename__ = "rooms"

    human_readable_id: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["UserModel"] = relationship(back_populates="owned_rooms")
    participants: Mapped[List["RoomParticipantModel"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    files: Mapped[List["FileMetadataModel"]] = relationship(back_populates="room", cascade="all, delete-orphan")

