from fastapi import APIRouter, status, UploadFile, File

from backend.room.dependencies.service import IRoomService
from backend.room.dto import RoomDTO
from backend.file.dto import FileMetadataDTO
from backend.security.dependencies import ICurrentUser
from backend.snapshot.dto import SnapshotDTO

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", response_model=RoomDTO, status_code=status.HTTP_201_CREATED)
async def create_room(current_user: ICurrentUser, service: IRoomService):
    return await service.create_room(current_user)

@router.post("/{room_id}/files", response_model=FileMetadataDTO, status_code=status.HTTP_201_CREATED)
async def upload_file(room_id: str, current_user: ICurrentUser, service: IRoomService, file: UploadFile = File(...)):
    return await service.upload_file_to_room(room_id, file, current_user)

@router.get("/{room_id}", response_model=RoomDTO)
async def get_room_details(room_id: str, service: IRoomService):
    return await service.get_room_details(room_id)

@router.post("/{room_id}/snapshots", response_model=SnapshotDTO, status_code=status.HTTP_201_CREATED)
async def create_snapshot(room_id: str, service: IRoomService, current_user: ICurrentUser):
    return await service.create_snapshot(room_id, current_user)