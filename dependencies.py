import time
from collections.abc import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import JWT_ALGORITHM, SECRET_KEY
from database import get_session
from models import User as UserModel


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")

class JWTTokenPayload(BaseModel):
    sub: str | int
    refresh: bool
    issued_at: int
    expires_at: int

async def on_auth(
        user: UserModel, 
        session: AsyncSession = Depends(get_session))-> UserModel:
    
    result = await session.execute(
        select(UserModel).where(UserModel.email == user.email)
        )
    
    if result.scalars().first() is not None:
        raise HTTPException(status_code = 400, detail = "Cannot use this email address")
    
    user = UserModel(
        name = user.name,
        email = user.email,
        # hashed_password = get_password_hash(user.password),
        hashed_password = user.password
    )

    session.add(user)
    await session.commit()
    
    return user 

async def get_current_user(
    session: AsyncSession = Depends(get_session), 
    token: str = Depends(reusable_oauth2)
) -> UserModel:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(UserModel).where(UserModel.id == token_data.sub))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return user
