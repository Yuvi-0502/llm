from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from ..models.user import UserRole

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
    notify_business: Optional[bool] = None
    notify_entertainment: Optional[bool] = None
    notify_sports: Optional[bool] = None
    notify_technology: Optional[bool] = None
    notify_keywords: Optional[bool] = None
    notification_keywords: Optional[str] = None

class UserInDB(UserBase):
    id: int
    role: UserRole
    is_active: bool
    notify_business: bool
    notify_entertainment: bool
    notify_sports: bool
    notify_technology: bool
    notify_keywords: bool
    notification_keywords: str

    class Config:
        from_attributes = True

class User(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None 