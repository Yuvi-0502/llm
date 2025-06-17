from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SavedArticleBase(BaseModel):
    user_id: int
    article_id: int
    saved_at: Optional[datetime] = None

class SavedArticleCreate(SavedArticleBase):
    pass

class SavedArticleOut(SavedArticleBase):
    saved_id: int

    class Config:
        orm_mode = True 