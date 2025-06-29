from backend.config.database.session import ISession
from backend.snapshot.models.snapshot import SnapshotModel


class SnapshotRepository:
    """Repository for snapshot data access."""
    def __init__(self, session: ISession):
        self.session = session

    async def create(self, room_id: int, archive_path: str) -> SnapshotModel:
        """
        Creates a new snapshot record in the database.

        Args:
            room_id (int): The ID of the room being snapshotted.
            archive_path (str): The path to the saved archive file.

        Returns:
            SnapshotModel: The created SQLAlchemy model instance.
        """
        instance = SnapshotModel(room_id=room_id, archive_path=archive_path)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance