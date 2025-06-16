from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: bool = False


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserResponse(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str 