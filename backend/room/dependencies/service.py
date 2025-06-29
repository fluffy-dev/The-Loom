from fastapi import Depends
from typing import Annotated

from backend.room.service import RoomService

IRoomService = Annotated[RoomService, Depends()]