from pydantic import BaseModel

class FileMetadataDTO(BaseModel):
    """
    Data Transfer Object for file metadata.
    """
    id: int
    original_name: str
    size_bytes: int

    class Config:
        from_attributes = True