from pydantic import BaseModel
from typing import Optional

class UserEnabledKeywordBase(BaseModel):
    keyword_id: int
    user_id: int
    is_enabled: Optional[bool] = True

class UserEnabledKeywordCreate(UserEnabledKeywordBase):
    pass

class UserEnabledKeywordOut(UserEnabledKeywordBase):
    id: int

    class Config:
        orm_mode = True 