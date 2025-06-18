from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    published_at: Optional[datetime] = None

class NewsArticleCreate(NewsArticleBase):
    server_id: int

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    category_id: Optional[int] = None

class NewsArticleResponse(NewsArticleBase):
    article_id: int
    category_id: Optional[int] = None
    server_id: int
    likes: int = 0
    dislikes: int = 0
    created_at: datetime

class NewsSearchRequest(BaseModel):
    query: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[str] = None
    sort_by: Optional[str] = "published_at"  # published_at, likes, dislikes
    page: int = 1
    page_size: int = 10