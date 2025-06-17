from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    user_id: int
    message: str
    is_read: Optional[bool] = False
    article_id: Optional[int] = None
    user_enabled_keyword_id: Optional[int] = None
    created_at: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationOut(NotificationBase):
    notification_id: int

    class Config:
        orm_mode = True 