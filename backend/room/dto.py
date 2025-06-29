from pydantic import BaseModel
from datetime import datetime


class RoomDTO(BaseModel):
    """
    Data Transfer Object for representing a room.
    """
    id: int
    human_readable_id: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True