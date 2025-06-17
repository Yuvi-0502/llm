from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    server_id: int

class ArticleCreate(ArticleBase):
    pass

class ArticleOut(ArticleBase):
    article_id: int

    class Config:
        orm_mode = True 