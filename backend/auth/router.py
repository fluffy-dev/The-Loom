from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.auth.dependencies.service import IAuthService
from backend.user.exceptions import UserNotFound
from backend.security.dto import TokenDTO

router = APIRouter(prefix="/auth", tags=["Authentication"])

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