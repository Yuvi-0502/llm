from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class ArticleCategory(Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    TECHNOLOGY = "technology"
    GENERAL = "general"

@dataclass
class Article:
    id: int
    title: str
    description: Optional[str]
    content: Optional[str]
    url: Optional[str]
    image_url: Optional[str]
    source_name: str
    source_id: Optional[str]
    author: Optional[str]
    published_at: datetime
    category: ArticleCategory
    likes: int
    dislikes: int

@dataclass
class ArticleSearchParams:
    query: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[ArticleCategory] = None
    sort_by: str = "published_at"
    sort_order: str = "desc" 