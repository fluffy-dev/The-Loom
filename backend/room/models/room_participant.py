from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base

class RoomParticipantModel(Base):
    """
    SQLAlchemy model representing a user's participation in a room.
    """
    __tablename__ = "room_participants"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))

    user: Mapped["UserModel"] = relationship(back_populates="participated_rooms")
    room: Mapped["RoomModel"] = relationship(back_populates="participants")