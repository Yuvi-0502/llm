from pydantic import BaseModel
from typing import Optional

class UserNotificationSettingBase(BaseModel):
    user_id: int
    category_id: int
    is_enabled: Optional[bool] = True

class UserNotificationSettingCreate(UserNotificationSettingBase):
    pass

class UserNotificationSettingOut(UserNotificationSettingBase):
    setting_id: int

    class Config:
        orm_mode = True 