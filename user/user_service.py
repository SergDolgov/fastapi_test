from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth_service import get_password_hash
from models import User

from user.user_schemas import UserCreateRequest, UserResponse, UserUpdatePasswordRequest

class UserService:

    async def delete(id: str, session: AsyncSession):
        """Delete user by id"""
        try:
            user = await session.get_one(User, id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))        

        await session.delete(user)
        await session.commit()
        return {"ok": True}

    async def getAll(session: AsyncSession):
            """getAll users"""

            try:
                statement = select(User)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))        

            return [user for user in await session.scalars(statement)]
               

    async def reset_password(user_update_password: UserUpdatePasswordRequest, current_user: User, session: AsyncSession) -> UserResponse:
        """Update current user password"""
        current_user.hashed_password = get_password_hash(user_update_password.password)
        session.add(current_user)
        await session.commit()
        return current_user


    async def get_one(id: int, session: AsyncSession) -> UserResponse:
        """Get product by id."""
        try:
            user = await session.get_one(User, id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))        

        return user


    async def register(new_user: UserCreateRequest, session: AsyncSession) -> UserResponse :
        """Create new user"""

        result = await session.execute(select(User).where(User.email == new_user.email))
        if result.scalars().first() is not None:
            raise HTTPException(status_code = 400, detail = "Cannot use this email address")
        user = User(
            name = new_user.name,
            email = new_user.email,
            hashed_password = get_password_hash(new_user.password),
        )
        session.add(user)
        await session.commit()
        return user    

