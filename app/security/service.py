from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.security.config import auth_config
from app.security.dto import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """
    Provides services for password hashing and verification.
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against a hashed one.

        Args:
            plain_password (str): The password in plain text.
            hashed_password (str): The hashed password from the database.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hashes a plain text password.

        Args:
            password (str): The password in plain text.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)


class AuthService:
    """
    Provides services for creating and validating JWT tokens.
    """

    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Creates a new JWT access token.

        Args:
            data (dict): The payload to encode in the token.

        Returns:
            str: The encoded JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM
        )

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        Creates a new JWT refresh token.

        Args:
            data (dict): The payload to encode in the token.

        Returns:
            str: The encoded JWT refresh token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=auth_config.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM
        )

    @staticmethod
    def verify_token(token: str) -> Optional[TokenPayload]:
        """
        Verifies a JWT token and decodes its payload.

        Args:
            token (str): The JWT token to verify.

        Returns:
            Optional[TokenPayload]: The decoded token payload if valid, otherwise None.
        """
        try:
            payload = jwt.decode(
                token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM]
            )
            return TokenPayload(**payload)
        except JWTError:
            return None