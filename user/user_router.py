from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth_service import get_password_hash

from dependencies import get_current_user, get_session
from models import User
from user.user_schemas import UserCreateRequest, UserResponse, UserUpdatePasswordRequest
from user.user_service import UserService


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/", response_model = list[UserResponse])
async def get_all(
    # current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get current user"""
    return await UserService.getAll(session)

@user_router.get("/{id}", response_model = UserResponse)
async def get_userById(
    id: int,
    # current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get user by Id"""
    user = await UserService.get_one(id, session)
    
    return user

@user_router.get("/me", response_model = UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Get current user"""
    return current_user

@user_router.delete("/me", status_code=204)
async def delete(id: str, session: AsyncSession = Depends(get_session)):
    """Delete user by id"""
    return UserService.delete(id, session)

@user_router.post("/reset-password", response_model = UserResponse)
async def reset_password(
    user_update_password: UserUpdatePasswordRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Update current user password"""
    return UserService.reset_password(user_update_password, current_user, session)


@user_router.post("/register", response_model = UserResponse)
async def register_new_user(
    new_user: UserCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    """Create new user"""
    # return UserService.register(new_user, session)
    # result = await session.execute(select(User).where(User.email == new_user.email))
    # if result.scalars().first() is not None:
    #     raise HTTPException(status_code = 400, detail = "Cannot use this email address")
    user = User(
        name = new_user.name,
        email = new_user.email,
        hashed_password = get_password_hash(new_user.password),
        identity = new_user.identity,
    )
    session.add(user)
    await session.commit()
    return user    
