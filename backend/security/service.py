from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.config.security import auth_config
from backend.security.dto import TokenPayloadDTO

# Используем bcrypt как основную и самую надежную схему хэширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """
    Provides services for password hashing and verification.
    """
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)


class TokenService:
    """
    Provides services for creating and validating JWT tokens.
    """
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=auth_config.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[TokenPayloadDTO]:
        try:
            payload = jwt.decode(
                token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM]
            )
            return TokenPayloadDTO(**payload)
        except JWTError:
            return None