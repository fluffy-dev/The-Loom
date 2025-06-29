from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File

from backend.room.service import RoomService
from backend.room.dto import RoomDTO
from backend.file.dto import FileMetadataDTO
from backend.room.repositories.room import RoomRepository
from backend.config.database.session import ISession
from backend.security.dependencies import ICurrentUser
from backend.room.exceptions import RoomLimitExceeded, RoomNotFound, FileLimitExceeded, FileSizeExceeded

router = APIRouter(prefix="/rooms", tags=["Rooms"])

def get_room_service(session: ISession) -> RoomService:
    """Dependency to provide the RoomService."""
    room_repo = RoomRepository(session)
    return RoomService(room_repo)

IRoomService = Annotated[RoomService, Depends(get_room_service)]

@router.post("/", response_model=RoomDTO, status_code=status.HTTP_201_CREATED)
async def create_room(current_user: ICurrentUser, service: IRoomService):
    """
    Creates a new collaboration room owned by the current user.
    """
    try:
        return await service.create_room(current_user)
    except RoomLimitExceeded as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.post("/{room_id}/files", response_model=FileMetadataDTO, status_code=status.HTTP_201_CREATED)
async def upload_file(
    room_id: str,
    current_user: ICurrentUser,
    service: IRoomService,
    file: UploadFile = File(...)
):
    """
    Uploads a file to a specific room.
    """
    try:
        return await service.upload_file_to_room(room_id, file, current_user)
    except RoomNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (FileLimitExceeded, FileSizeExceeded) as e:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(e))