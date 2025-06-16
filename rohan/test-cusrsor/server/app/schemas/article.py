from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: HttpUrl
    source: str
    published_at: datetime
    category_id: Optional[int] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    source: Optional[str] = None
    published_at: Optional[datetime] = None


class ArticleInDBBase(ArticleBase):
    id: int
    likes: int = 0
    dislikes: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ArticleResponse(ArticleInDBBase):
    pass


class ArticleInDB(ArticleInDBBase):
    pass 