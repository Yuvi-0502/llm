from sqlalchemy import Column, String, Integer, ForeignKey, Table, JSON, Enum
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import enum

class NewsCategory(str, enum.Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    TECHNOLOGY = "technology"
    GENERAL = "general"

# Association table for saved articles
user_saved_articles = Table(
    'user_saved_articles',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('article_id', Integer, ForeignKey('news_articles.id'))
)

class NewsArticle(BaseModel):
    __tablename__ = "news_articles"

    title = Column(String, nullable=False)
    description = Column(String)
    content = Column(String)
    url = Column(String)
    image_url = Column(String)
    source = Column(String)
    category = Column(Enum(NewsCategory), default=NewsCategory.GENERAL)
    published_at = Column(String)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    raw_data = Column(JSON)  # Store the complete API response

    # Relationships
    saved_by = relationship("User", secondary=user_saved_articles, backref="saved_articles") 