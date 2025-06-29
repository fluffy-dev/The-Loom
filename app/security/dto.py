from pydantic import BaseModel

class Token(BaseModel):
    """
    DTO for representing JWT access and refresh tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    DTO for the payload data encoded within the JWT.
    """
    sub: str | None = None