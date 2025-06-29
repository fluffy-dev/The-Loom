from redis.asyncio import Redis
from backend.redis_client.client import get_redis_client

# Ключи для хранения данных в Redis
# Y-Py документы для каждого файла
YDOC_KEY = "ydoc:{room_id}:{file_id}"
# Состояние присутствия (курсоры, имена) для комнаты
AWARENESS_KEY = "awareness:{room_id}"

class CollaborationService:
    """
    Service to manage the persistence of CRDT data in Redis.
    """
    def __init__(self):
        """Initializes the service with a Redis client."""
        self.redis: Redis = get_redis_client()

    async def get_document_state(self, room_id: str, file_id: str) -> bytes | None:
        """
        Retrieves the latest state of a CRDT document from Redis.

        Args:
            room_id (str): The ID of the room.
            file_id (str): The ID of the file.

        Returns:
            bytes | None: The binary document state, or None if it doesn't exist.
        """
        key = YDOC_KEY.format(room_id=room_id, file_id=file_id)
        return await self.redis.get(key)

    async def save_document_state(self, room_id: str, file_id: str, data: bytes):
        """
        Saves the state of a CRDT document to Redis.

        Args:
            room_id (str): The ID of the room.
            file_id (str): The ID of the file.
            data (bytes): The binary document state to save.
        """
        key = YDOC_KEY.format(room_id=room_id, file_id=file_id)
        await self.redis.set(key, data)

    # Методы для awareness можно добавить здесь по аналогии, если потребуется
    # более сложная логика, чем просто ретрансляция.