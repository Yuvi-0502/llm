from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    id: int
    title: str
    content: str
    url: str
    source: str
    category: str
    published_at: datetime
    created_at: datetime 