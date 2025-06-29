from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from backend.user.exceptions import UserAlreadyExist, UserNotFound
from backend.config.database.session import ISession
from backend.user.models.user import UserModel
from backend.user.dto import UpdateUserDTO, UserDTO, FindUserDTO


class UserRepository:
    """
    Repository for user data access, operating with DTOs.
    """
    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, user: UserDTO) -> UserDTO:
        instance = UserModel(
            name=user.name,
            login=user.login,
            email=user.email,
            password=user.password # Expects hashed password
        )
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
            return self._get_dto(instance)
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExist

    async def get(self, pk: int) -> Optional[UserDTO]:
        instance = await self.session.get(UserModel, pk)
        if instance is None:
            raise UserNotFound
        return self._get_dto(instance)

    async def find(self, dto: FindUserDTO) -> Optional[UserDTO]:
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance is None:
            raise UserNotFound
        return self._get_dto(instance)

    async def get_list(self, limit: int = 100, offset: int = 0) -> List[UserDTO]:
        stmt = select(UserModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def update(self, dto: UpdateUserDTO, pk: int) -> UserDTO:
        stmt = (
            update(UserModel)
            .values(**dto.model_dump(exclude_none=True))
            .where(UserModel.id == pk)
            .returning(UserModel)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        instance = result.scalar_one_or_none()
        if instance is None:
            raise UserNotFound
        return self._get_dto(instance)

    @staticmethod
    def _get_dto(instance: UserModel) -> UserDTO:
        return UserDTO(
            id=instance.id,
            name=instance.name,
            login=instance.login,
            email=instance.email,
            password=instance.password
        )