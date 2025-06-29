from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserDTO(BaseModel):
    id: Optional[int] = None
    name: constr(max_length=30)
    login: constr(max_length=50)
    email: EmailStr
    password: Optional[str] = None

class PublicUserDTO(BaseModel):
    name: constr(max_length=30)

class PrivateUserDTO(BaseModel):
    name: constr(max_length=30)
    login: constr(max_length=50)
    email: EmailStr

class FindUserDTO(BaseModel):
    id: Optional[int] = None
    login: Optional[constr(max_length=50)] = None
    email: Optional[EmailStr] = None

class UpdateUserDTO(BaseModel):
    name: Optional[constr(max_length=30)] = None
    login: Optional[constr(max_length=50)] = None