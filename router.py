from __future__ import annotations
from typing import Annotated

from fastapi import APIRouter, Depends

from user.repository import UserRepository
from schemas import SUserAdd, SUser, SUserId

router = APIRouter(
    prefix="/users",
    tags=["Таски"],
)


@router.post("")
async def add_user(
        user: Annotated[SUserAdd, Depends()],
) -> SUserId:
    user_id = await UserRepository.add_one(user)
    return {"ok": True, "user_id": user_id}


@router.get("")
async def get_users() -> list[SUser]:
    users = await UserRepository.find_all()
    return users
