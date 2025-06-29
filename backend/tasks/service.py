import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.config.database.session import ISession
from backend.config.tasks import task_settings
from backend.room.models.room import RoomModel
from backend.redis_client.client import get_redis_client


class CleanupService:
    """
    Provides services for cleaning up expired and inactive rooms.
    """

    def __init__(self, session: ISession):
        """
        Initializes the CleanupService.

        Args:
            session (ISession): The database session dependency.
        """
        self.session = session
        self.redis = get_redis_client()

    async def find_and_delete_expired_rooms(self):
        """
        Finds all expired rooms and orchestrates their deletion.

        A room is considered expired if it was created more than
        ROOM_LIFETIME_DAYS ago, or if it has been inactive for more than
        ROOM_INACTIVITY_HOURS.
        """
        expired_rooms = await self._get_expired_rooms()
        for room in expired_rooms:
            self._delete_room_files(room)
            await self._delete_room_from_db(room)

    async def _get_expired_rooms(self) -> list[RoomModel]:
        """
        Retrieves a list of expired room models from the database.

        This method queries for rooms based on their creation date and
        last activity timestamp stored in Redis.

        Returns:
            list[RoomModel]: A list of SQLAlchemy RoomModel instances to be deleted.
        """
        now = datetime.now(timezone.utc)
        lifetime_threshold = now - timedelta(days=task_settings.ROOM_LIFETIME_DAYS)
        inactivity_threshold = now - timedelta(hours=task_settings.ROOM_INACTIVITY_HOURS)

        # 1. Получаем все комнаты, устаревшие по сроку жизни
        stmt_lifetime = (
            select(RoomModel)
            .options(
                selectinload(RoomModel.files),
                selectinload(RoomModel.snapshots)
            )
            .where(RoomModel.created_at < lifetime_threshold)
        )
        result = await self.session.execute(stmt_lifetime)
        expired_by_lifetime = list(result.scalars().all())
        expired_ids = {room.id for room in expired_by_lifetime}

        # 2. Проверяем неактивные комнаты
        inactive_room_keys = await self.redis.keys("activity:*")
        inactive_rooms_to_check = []

        for key in inactive_room_keys:
            last_active_str = await self.redis.get(key)
            last_active = datetime.fromisoformat(last_active_str.decode())
            if last_active.replace(tzinfo=timezone.utc) < inactivity_threshold:
                room_id = int(key.decode().split(":")[1])
                if room_id not in expired_ids:
                    inactive_rooms_to_check.append(room_id)

        if inactive_rooms_to_check:
            stmt_inactive = (
                select(RoomModel)
                .options(
                    selectinload(RoomModel.files),
                    selectinload(RoomModel.snapshots)
                )
                .where(RoomModel.id.in_(inactive_rooms_to_check))
            )
            result = await self.session.execute(stmt_inactive)
            expired_by_inactivity = list(result.scalars().all())
            return expired_by_lifetime + expired_by_inactivity

        return expired_by_lifetime

    def _delete_room_files(self, room: RoomModel):
        """
        Deletes all associated files and snapshots of a room from the disk.

        Args:
            room (RoomModel): The room whose files are to be deleted.
        """
        for file_meta in room.files:
            if Path(file_meta.disk_path).exists():
                os.remove(file_meta.disk_path)

        for snapshot in room.snapshots:
            if Path(snapshot.archive_path).exists():
                os.remove(snapshot.archive_path)

    async def _delete_room_from_db(self, room: RoomModel):
        """
        Deletes a room and all its related data from the database.

        Leverages `cascade="all, delete-orphan"` in model relationships to
        automatically remove related participants, files, and snapshots.

        Args:
            room (RoomModel): The room model instance to delete.
        """
        await self.session.delete(room)
        await self.session.commit()
        await self.redis.delete(f"activity:{room.id}")