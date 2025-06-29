from fastapi import APIRouter, status, HTTPException, UploadFile, File

from backend.room.dependencies.service import IRoomService
from backend.room.dto import RoomDTO
from backend.file.dto import FileMetadataDTO
from backend.security.dependencies import ICurrentUser
from backend.room.exceptions import RoomLimitExceeded, RoomNotFound, FileLimitExceeded, FileSizeExceeded
from backend.snapshot.dto import SnapshotDTO

router = APIRouter(prefix="/rooms", tags=["Rooms"])

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

@router.get("/{room_id}", response_model=RoomDTO)
async def get_room_details(room_id: str, service: IRoomService):
    """
    Retrieves detailed information about a room, including its files and snapshots.
    """
    try:
        return await service.get_room_details(room_id)
    except RoomNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{room_id}/snapshots", response_model=SnapshotDTO, status_code=status.HTTP_201_CREATED)
async def create_snapshot(room_id: str, service: IRoomService):
    """
    Creates a point-in-time snapshot of all files in the room.
    """
    try:
        return await service.create_snapshot(room_id)
    except RoomNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))