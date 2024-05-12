import time

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import JWT_ALGORITHM, SECRET_KEY
from database import get_session
from models import User
from auth.auth_schemas import AccessTokenResponse, RefreshTokenRequest
from auth.auth_service import JWTTokenPayload, generate_access_token_response, verify_password


auth_router = APIRouter()


@auth_router.post("/access-token", response_model=AccessTokenResponse)
async def login_access_token(
    session: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """OAuth2 compatible token, get an access token for future requests using username and password"""

    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return generate_access_token_response(str(user.id))


@auth_router.post("/refresh-token", response_model = AccessTokenResponse)
async def refresh_token(
    input: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
):
    """OAuth2 compatible token, get an access token for future requests using refresh token"""
    try:
        payload = jwt.decode(
            jwt=input.refresh_token,
            key=SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, unknown error",
        )

    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = JWTTokenPayload(**payload)

    if not token_data.refresh:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use access token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return generate_access_token_response(str(user.id))
