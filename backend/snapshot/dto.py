from pydantic import BaseModel
from datetime import datetime

class SnapshotDTO(BaseModel):
    """
    Data Transfer Object for snapshot information.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True