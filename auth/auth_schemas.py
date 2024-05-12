
from pydantic import BaseModel, EmailStr

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int