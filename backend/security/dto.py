from pydantic import BaseModel

class TokenDTO(BaseModel):
    """
    DTO for representing JWT access and refresh tokens.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayloadDTO(BaseModel):
    """
    DTO for the payload data encoded within the JWT.
    'sub' (subject) will typically be the user's ID.
    """
    sub: str | None = None