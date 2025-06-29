from fastapi import Depends
from typing import Annotated

from backend.room.repositories.room import RoomRepository


IRoomRepository = Annotated[RoomRepository, Depends()]