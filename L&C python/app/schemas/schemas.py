from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# News Article schemas
class NewsArticleBase(BaseModel):
    title: str
    description: str
    content: str
    url: str
    image_url: Optional[str] = None
    source: str
    category: str
    published_at: datetime

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None

class NewsArticleInDB(NewsArticleBase):
    id: int
    created_at: datetime
    likes: int
    dislikes: int

    class Config:
        from_attributes = True

# Category schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# External Server schemas
class ExternalServerBase(BaseModel):
    name: str
    api_key: str
    base_url: str
    is_active: bool = True

class ExternalServerCreate(ExternalServerBase):
    pass

class ExternalServerUpdate(BaseModel):
    name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    is_active: Optional[bool] = None

class ExternalServerInDB(ExternalServerBase):
    id: int
    last_accessed: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Notification schemas
class NotificationBase(BaseModel):
    title: str
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationInDB(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Notification Preference schemas
class NotificationPreferenceBase(BaseModel):
    category: str
    is_enabled: bool
    keywords: Optional[str] = None

class NotificationPreferenceCreate(NotificationPreferenceBase):
    user_id: int

class NotificationPreferenceUpdate(BaseModel):
    is_enabled: Optional[bool] = None
    keywords: Optional[str] = None

class NotificationPreferenceInDB(NotificationPreferenceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 