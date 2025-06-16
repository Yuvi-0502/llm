from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class ArticleCategory(enum.Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    SPORTS = "sports"
    TECHNOLOGY = "technology"
    GENERAL = "general"

# Association table for saved articles
saved_articles = Table(
    'saved_articles',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('article_id', Integer, ForeignKey('articles.id'))
)

class Article(BaseModel):
    __tablename__ = "articles"

    title = Column(String(200), nullable=False)
    description = Column(Text)
    content = Column(Text)
    url = Column(String(500))
    image_url = Column(String(500))
    source_name = Column(String(100))
    source_id = Column(String(100))
    author = Column(String(100))
    published_at = Column(DateTime)
    category = Column(Enum(ArticleCategory), default=ArticleCategory.GENERAL)
    
    # Engagement metrics
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    
    # Relationships
    saved_by = relationship("User", secondary=saved_articles, backref="saved_articles") 