from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from ..models.article import ArticleCategory

class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    source_name: str
    source_id: Optional[str] = None
    author: Optional[str] = None
    category: ArticleCategory

class ArticleCreate(ArticleBase):
    published_at: datetime

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    category: Optional[ArticleCategory] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None

class ArticleInDB(ArticleBase):
    id: int
    published_at: datetime
    likes: int
    dislikes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Article(ArticleInDB):
    pass

class ArticleSearchParams(BaseModel):
    query: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[ArticleCategory] = None
    sort_by: Optional[str] = "published_at"  # published_at, likes, dislikes
    sort_order: Optional[str] = "desc"  # asc, desc 