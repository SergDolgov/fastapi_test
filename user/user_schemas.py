
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreateRequest(BaseModel):
    name: str 
    email: EmailStr
    password: str
    identity: str | None = 'None'
    class Config:
         from_attributes = True

class UserUpdatePasswordRequest(BaseModel):
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr  
    # model_config = ConfigDict(from_attributes=True)
    # model_config = ConfigDict(coerce_numbers_to_str=True)
    
    class Config:
         from_attributes = True