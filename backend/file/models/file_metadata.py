from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base

class FileMetadataModel(Base):
    """
    SQLAlchemy model for file metadata.

    Attributes:
        original_name (Mapped[str]): The original name of the file as uploaded by the user.
        disk_path (Mapped[str]): The path to the file on the server's local storage.
        size_bytes (Mapped[int]): The size of the file in bytes.
        room_id (Mapped[int]): The ID of the room this file belongs to.
        room (Mapped["RoomModel"]): Relationship to the parent room.
    """
    __tablename__ = "file_metadata"

    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    disk_path: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    room: Mapped["RoomModel"] = relationship(back_populates="files")