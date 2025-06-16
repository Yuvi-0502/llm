from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from app.models.user import UserRole

# Request DTOs
class UserLoginDTO(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class UserRegistrationDTO(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)
    role: UserRole = UserRole.USER

class UserUpdateDTO(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, max_length=50)] = None
    password: Optional[constr(min_length=8)] = None
    is_active: Optional[bool] = None

class NotificationPreferencesDTO(BaseModel):
    notify_business: Optional[bool] = None
    notify_entertainment: Optional[bool] = None
    notify_sports: Optional[bool] = None
    notify_technology: Optional[bool] = None
    notify_keywords: Optional[bool] = None
    notification_keywords: Optional[List[str]] = None

# Response DTOs
class UserResponseDTO(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    notify_business: bool
    notify_entertainment: bool
    notify_sports: bool
    notify_technology: bool
    notify_keywords: bool
    notification_keywords: List[str]

    class Config:
        from_attributes = True

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str

class UserListResponseDTO(BaseModel):
    users: List[UserResponseDTO]
    total: int
    page: int
    size: int 