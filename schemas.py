from typing import Optional

from pydantic import BaseModel, ConfigDict


class SUserAdd(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = 'users'

class SUser(SUserAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SUserId(BaseModel):
    ok: bool = True
    user_id: int

class SCompany(BaseModel):
    id: Optional[int]
    name: str
    owner_id: int

    class Config:
        orm_mode = True

class SEmployee(BaseModel):
    id: Optional[int]
    fullName: str
    company_id: int
    dept_id: Optional[int]
    user_id: Optional[int]
    acc_id: Optional[int]
    salary: int

    class Config:
        orm_mode = True

class SDepartment(BaseModel):
    id: Optional[int]
    name: str
    company_id: int
    manager_id: Optional[int]

    class Config:
        orm_mode = True

class SBankAccount(BaseModel):
    id: Optional[int]
    company_id: int
    bank: str
    name: str

    class Config:
        orm_mode = True

