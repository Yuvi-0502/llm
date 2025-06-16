from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class NotificationBase(BaseModel):
    message: str
    created_at: datetime


class NotificationResponse(NotificationBase):
    id: int

    class Config:
        orm_mode = True


class NotificationPreferences(BaseModel):
    categories: Dict[str, bool] 