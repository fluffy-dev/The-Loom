from fastapi.security import OAuth2PasswordRequestForm

from backend.user.dependencies.repository import IUserRepository
from backend.user.exceptions import UserNotFound
from backend.security.service import PasswordService, TokenService
from backend.security.dto import TokenDTO

class AuthService:
    """
    Service layer for authentication logic.
    """
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def login(self, form_data: OAuth2PasswordRequestForm) -> TokenDTO:
        """
        Authenticates a user and issues JWT tokens.

        Args:
            form_data (OAuth2PasswordRequestForm): The user's login and password.

        Returns:
            TokenDTO: A DTO containing the access and refresh tokens.

        Raises:
            UserNotFound: If the user does not exist or password is incorrect.
        """
        user = await self.user_repo.find({"login": form_data.username})
        if not user:
            raise UserNotFound

        if not PasswordService.verify_password(form_data.password, user.password):
            raise UserNotFound

        access_token = TokenService.create_access_token(data={"sub": str(user.id)})
        refresh_token = TokenService.create_refresh_token(data={"sub": str(user.id)})

        return TokenDTO(access_token=access_token, refresh_token=refresh_token)