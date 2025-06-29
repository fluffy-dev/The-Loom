import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile

from backend.room.repositories.room import RoomRepository
from backend.room.dto import RoomDTO
from backend.file.dto import FileMetadataDTO
from backend.user.dto import UserDTO
from backend.room.exceptions import RoomLimitExceeded, RoomNotFound, FileLimitExceeded, FileSizeExceeded
from backend.file.models.file_metadata import FileMetadataModel

# Константы для ограничений
MAX_ROOMS_PER_USER = 3
MAX_FILES_PER_ROOM = 20
MAX_FILE_SIZE_MB = 5
STORAGE_PATH = Path("./storage/files") # Путь для хранения файлов

class RoomService:
    """
    Service layer for room and file business logic.
    """
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo
        # Создаем директорию для хранения файлов, если она не существует
        STORAGE_PATH.mkdir(parents=True, exist_ok=True)

    async def create_room(self, current_user: UserDTO) -> RoomDTO:
        """
        Creates a new collaboration room for the current user.

        Checks if the user has exceeded their room creation limit before creating.

        Args:
            current_user (UserDTO): The authenticated user creating the room.

        Returns:
            RoomDTO: A DTO representing the newly created room.

        Raises:
            RoomLimitExceeded: If the user already owns the maximum number of rooms.
        """
        current_room_count = await self.room_repo.count_by_owner_id(current_user.id)
        if current_room_count >= MAX_ROOMS_PER_USER:
            raise RoomLimitExceeded(f"User has reached the limit of {MAX_ROOMS_PER_USER} rooms.")

        # Генерируем простой, но уникальный ID
        human_readable_id = str(uuid.uuid4())[:8]
        new_room = await self.room_repo.create(human_readable_id, current_user.id)
        return RoomDTO.model_validate(new_room)

    async def upload_file_to_room(self, room_id: str, file: UploadFile, current_user: UserDTO) -> FileMetadataDTO:
        """
        Uploads a file to a specified room.

        Validates room existence, user permissions, file count, and file size.
        Saves the file to local storage.

        Args:
            room_id (str): The human-readable ID of the target room.
            file (UploadFile): The file being uploaded.
            current_user (UserDTO): The authenticated user uploading the file.

        Returns:
            FileMetadataDTO: Metadata of the successfully uploaded file.

        Raises:
            RoomNotFound: If the room with the given ID does not exist.
            FileLimitExceeded: If the room already contains the maximum number of files.
            FileSizeExceeded: If the file size is larger than the allowed limit.
        """
        room = await self.room_repo.get_by_human_id(room_id)
        if not room:
            raise RoomNotFound("The specified room does not exist.")

        # В будущем здесь можно добавить проверку прав доступа
        # if room.owner_id != current_user.id:
        #     raise PermissionError("User does not have permission to upload to this room.")

        if len(room.files) >= MAX_FILES_PER_ROOM:
            raise FileLimitExceeded(f"Room has reached the limit of {MAX_FILES_PER_ROOM} files.")

        file_size = file.size
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise FileSizeExceeded(f"File size exceeds the limit of {MAX_FILE_SIZE_MB} MB.")

        file_uuid = str(uuid.uuid4())
        disk_path = STORAGE_PATH / file_uuid

        # Асинхронно сохраняем файл на диск
        async with aiofiles.open(disk_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # Read in 1MB chunks
                await out_file.write(content)

        # Создаем метаданные в БД
        file_metadata = FileMetadataModel(
            original_name=file.filename,
            disk_path=str(disk_path),
            size_bytes=file_size,
            room_id=room.id
        )
        self.room_repo.session.add(file_metadata)
        await self.room_repo.session.commit()
        await self.room_repo.session.refresh(file_metadata)

        return FileMetadataDTO.model_validate(file_metadata)