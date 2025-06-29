from typing import List

from backend.libs.exceptions import PaginationError
from backend.user.dependencies.repository import IUserRepository
from backend.user.dto import UserDTO, UpdateUserDTO, FindUserDTO, PublicUserDTO, PrivateUserDTO
# We will need PasswordService later for real user creation
# from src.security.service import PasswordService

class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.repository = user_repository

    async def create_user_with_hashed_password(self, dto: UserDTO) -> PrivateUserDTO:
        """
        Creates a new user, hashing the password before saving.
        This is a placeholder for a more complete security implementation.
        """
        # In a real scenario, you'd use a robust password hashing service.
        # For now, we'll just append a suffix for demonstration.
        # dto.password = PasswordService.get_password_hash(dto.password)
        dto.password = dto.password + "_hashed"

        created_user = await self.repository.create(dto)
        return PrivateUserDTO(
            name=created_user.name,
            login=created_user.login,
            email=created_user.email,
        )

    async def get_user_public_profile(self, pk: int) -> PublicUserDTO:
        user = await self.repository.get(pk)
        return PublicUserDTO(name=user.name)

    async def get_user_private_profile(self, pk: int) -> PrivateUserDTO:
        user = await self.repository.get(pk)
        return PrivateUserDTO(name=user.name, login=user.login, email=user.email)

    async def get_users_list(self, limit: int = 100, offset: int = 0) -> List[PublicUserDTO]:
        if limit < 0 or offset < 0:
            raise PaginationError("Limit and offset must be non-negative")
        users = await self.repository.get_list(limit, offset)
        return [PublicUserDTO(name=user.name) for user in users]