from pydantic import BaseModel
from datetime import datetime
from typing import List
from backend.file.dto import FileMetadataDTO
from backend.snapshot.dto import SnapshotDTO


class RoomDTO(BaseModel):
    """
    Data Transfer Object for representing a room.
    """
    id: int
    human_readable_id: str
    owner_id: int
    files: List[FileMetadataDTO]
    snapshots: List[SnapshotDTO]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True