from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.auth.service import AuthService
from backend.user.dependencies.repository import IUserRepository
from backend.user.exceptions import UserNotFound
from backend.security.dto import TokenDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_service(user_repo: IUserRepository) -> AuthService:
    """
    Dependency to provide the AuthService.
    """
    return AuthService(user_repo)

IAuthService = Annotated[AuthService, Depends(get_auth_service)]

@router.post("/token", response_model=TokenDTO)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: IAuthService
):
    """
    Provides access and refresh tokens for a valid user.
    """
    try:
        tokens = await service.login(form_data)
        return tokens
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )