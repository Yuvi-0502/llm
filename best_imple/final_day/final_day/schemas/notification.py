from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NotificationBase(BaseModel):
    title: str
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    notification_id: int
    user_id: int
    is_read: bool
    created_at: datetime

class UserPreferenceBase(BaseModel):
    category_id: Optional[int] = None
    keywords: Optional[str] = None
    email_notifications: bool = True

class UserPreferenceCreate(UserPreferenceBase):
    user_id: int

class UserPreferenceUpdate(BaseModel):
    category_id: Optional[int] = None
    keywords: Optional[str] = None
    email_notifications: Optional[bool] = None

class UserPreferenceResponse(UserPreferenceBase):
    preference_id: int
    user_id: int
    created_at: datetime 