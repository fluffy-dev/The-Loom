from fastapi import Depends
from typing import Annotated

from backend.auth.service import AuthService

IAuthService = Annotated[AuthService, Depends()]