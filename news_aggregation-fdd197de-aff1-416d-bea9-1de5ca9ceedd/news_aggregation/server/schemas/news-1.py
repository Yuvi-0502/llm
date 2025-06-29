from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NewsArticleCreate(BaseModel):
    server_id: int
    title: str
    description: Optional[str]
    content: Optional[str]
    source: Optional[str]
    url: str
    published_at: Optional[datetime]
    categories: Optional[List[str]] = []


class NewsArticle(BaseModel):
    article_id: int
    server_id: int
    title: str
    description: Optional[str]
    content: Optional[str]
    source: Optional[str]
    url: str
    published_at: Optional[datetime]