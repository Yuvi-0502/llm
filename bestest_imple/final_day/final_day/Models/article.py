from pydantic import BaseModel
from typing import Optional
from datetime import  datetime


class Article(BaseModel):
    article_id: int
    title: str
    description: str
    keywords: str
    url: str
    published_at: datetime
    external_api_server_id: int

