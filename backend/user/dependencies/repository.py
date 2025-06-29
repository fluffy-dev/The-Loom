from fastapi import Depends
from typing import Annotated
from backend.user.repositories.user import UserRepository

IUserRepository = Annotated[UserRepository, Depends()]