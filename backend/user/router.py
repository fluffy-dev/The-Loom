from fastapi import APIRouter, status, HTTPException
from typing import List

from backend.user.dependencies.service import IUserService
from backend.user.dto import UserDTO, PublicUserDTO, PrivateUserDTO
from backend.libs.exceptions import AlreadyExists, NotFound, PaginationError
from backend.security.dependencies import ICurrentUser


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PrivateUserDTO)
async def register_user(user_data: UserDTO, service: IUserService):
    try:
        return await service.create_user_with_hashed_password(user_data)
    except AlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this login or email already exists."
        )

@router.get("/{user_id}", response_model=PublicUserDTO)
async def get_user_public_profile(user_id: int, service: IUserService):
    try:
        return await service.get_user_public_profile(user_id)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")

@router.get("/", response_model=List[PublicUserDTO])
async def get_all_users(service: IUserService, limit: int = 100, offset: int = 0):
    try:
        return await service.get_users_list(limit, offset)
    except PaginationError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

@router.get("/me", response_model=PrivateUserDTO, summary="Get current user profile")
async def read_users_me(current_user: ICurrentUser):
    """
    Retrieves the private profile of the currently authenticated user.
    """
    return PrivateUserDTO(
        name=current_user.name,
        login=current_user.login,
        email=current_user.email
    )