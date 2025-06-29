from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from backend.config.database.session import ISession
from backend.room.models.room import RoomModel
from backend.room.models.room_participant import RoomParticipantModel


class RoomRepository:
    """
    Repository for room data access.
    """
    def __init__(self, session: ISession):
        self.session = session

    async def create(self, human_readable_id: str, owner_id: int) -> RoomModel:
        """
        Creates a new room instance in the database.

        Args:
            human_readable_id (str): The user-friendly ID for the room.
            owner_id (int): The ID of the user who owns the room.

        Returns:
            RoomModel: The created SQLAlchemy model instance.
        """
        instance = RoomModel(human_readable_id=human_readable_id, owner_id=owner_id)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def count_by_owner_id(self, owner_id: int) -> int:
        """
        Counts the number of rooms owned by a specific user.

        Args:
            owner_id (int): The ID of the user.

        Returns:
            int: The total count of rooms owned by the user.
        """
        stmt = select(func.count(RoomModel.id)).where(RoomModel.owner_id == owner_id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_by_human_id(self, human_readable_id: str) -> RoomModel | None:
        """
        Retrieves a room by its human-readable ID, preloading files and snapshots.
        """
        stmt = (
            select(RoomModel)
            .where(RoomModel.human_readable_id == human_readable_id)
            .options(
                selectinload(RoomModel.files),
                selectinload(RoomModel.snapshots)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_rooms_for_user(self, user_id: int) -> List[RoomModel]:
        """
        Retrieves all rooms a user has participated in.
        """
        stmt = (
            select(RoomModel)
            .join(RoomParticipantModel)
            .where(RoomParticipantModel.user_id == user_id)
            .order_by(RoomModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())