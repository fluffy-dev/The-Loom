from fastapi import APIRouter, status
from typing import List

from backend.room.dto import RoomDTO
from backend.user.dependencies.service import IUserService
from backend.user.dto import UserDTO, PublicUserDTO, PrivateUserDTO
from backend.security.dependencies import ICurrentUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PrivateUserDTO)
async def register_user(user_data: UserDTO, service: IUserService):
    return await service.create_user_with_hashed_password(user_data)

@router.get("/{user_id}", response_model=PublicUserDTO)
async def get_user_public_profile(user_id: int, service: IUserService):
    return await service.get_user_public_profile(user_id)

@router.get("/", response_model=List[PublicUserDTO])
async def get_all_users(service: IUserService, limit: int = 100, offset: int = 0):
    return await service.get_users_list(limit, offset)

@router.get("/me", response_model=PrivateUserDTO, summary="Get current user profile")
async def read_users_me(current_user: ICurrentUser):
    return PrivateUserDTO(name=current_user.name, login=current_user.login, email=current_user.email)

@router.get("/me/rooms", response_model=List[RoomDTO])
async def get_my_rooms(current_user: ICurrentUser, service: IUserService):
    return await service.get_user_rooms(current_user.id)