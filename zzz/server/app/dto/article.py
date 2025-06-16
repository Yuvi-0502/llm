from typing import Optional, List
from pydantic import BaseModel, HttpUrl, constr
from datetime import datetime
from app.models.article import ArticleCategory

# Request DTOs
class ArticleCreateDTO(BaseModel):
    title: constr(min_length=1, max_length=200)
    description: constr(min_length=1, max_length=500)
    content: constr(min_length=1)
    url: HttpUrl
    image_url: Optional[HttpUrl] = None
    source_name: constr(min_length=1, max_length=100)
    source_id: Optional[int] = None
    author: Optional[constr(max_length=100)] = None
    published_at: datetime
    category: Optional[ArticleCategory] = None

class ArticleUpdateDTO(BaseModel):
    title: Optional[constr(min_length=1, max_length=200)] = None
    description: Optional[constr(min_length=1, max_length=500)] = None
    content: Optional[constr(min_length=1)] = None
    url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    source_name: Optional[constr(min_length=1, max_length=100)] = None
    source_id: Optional[int] = None
    author: Optional[constr(max_length=100)] = None
    published_at: Optional[datetime] = None
    category: Optional[ArticleCategory] = None

class ArticleSearchDTO(BaseModel):
    query: Optional[str] = None
    category: Optional[ArticleCategory] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_confidence: Optional[float] = 0.0
    sort_by: Optional[str] = "published_at"
    sort_order: Optional[str] = "desc"

# Response DTOs
class ArticleResponseDTO(BaseModel):
    id: int
    title: str
    description: str
    content: str
    url: str
    image_url: Optional[str]
    source_name: str
    source_id: Optional[int]
    author: Optional[str]
    published_at: datetime
    category: ArticleCategory
    category_confidence: float
    likes: int
    dislikes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ArticleListResponseDTO(BaseModel):
    articles: List[ArticleResponseDTO]
    total: int
    page: int
    size: int

class ArticleCategoryResponseDTO(BaseModel):
    category: ArticleCategory
    count: int
    confidence_avg: float 