from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from src.models._enum import UserRole

class UserCreate(BaseModel):
    email:EmailStr
    password: str = Field(min_length=8)
    role:UserRole = 'EMPLOYEE'
    is_active:bool = True

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active:bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    email:str
    access_token:str
    token_type:str

    model_config = ConfigDict(from_attributes=True)