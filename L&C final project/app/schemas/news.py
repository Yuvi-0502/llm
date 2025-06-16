from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from app.models.news import NewsCategory

class NewsArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: HttpUrl
    image_url: Optional[HttpUrl] = None
    source: str
    category: NewsCategory = NewsCategory.GENERAL
    published_at: str

class NewsArticleCreate(NewsArticleBase):
    raw_data: dict

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    source: Optional[str] = None
    category: Optional[NewsCategory] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None

class NewsArticleInDB(NewsArticleBase):
    id: int
    likes: int
    dislikes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class NewsArticle(NewsArticleInDB):
    pass

class NewsArticleList(BaseModel):
    articles: List[NewsArticle]
    total: int
    page: int
    size: int

class NewsSearchParams(BaseModel):
    query: str
    category: Optional[NewsCategory] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_by: Optional[str] = None  # 'likes', 'dislikes', 'date'
    page: int = 1
    size: int = 10 