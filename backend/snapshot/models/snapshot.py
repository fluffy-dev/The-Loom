from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base

class SnapshotModel(Base):
    """
    SQLAlchemy model for a room snapshot.

    A snapshot represents a point-in-time backup of all files in a room,
    stored as a single archive file.

    Attributes:
        archive_path (Mapped[str]): The path to the snapshot's .zip archive file.
        room_id (Mapped[int]): The ID of the room this snapshot belongs to.
        room (Mapped["RoomModel"]): Relationship to the parent room.
    """
    __tablename__ = "snapshots"

    archive_path: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    room: Mapped["RoomModel"] = relationship(back_populates="snapshots")