from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

# Association table for many-to-many relationship between users and saved articles
user_saved_articles = Table(
    'user_saved_articles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('article_id', Integer, ForeignKey('news_articles.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    saved_articles = relationship("NewsArticle", secondary=user_saved_articles, back_populates="saved_by_users")
    notifications = relationship("Notification", back_populates="user")

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    content = Column(Text)
    url = Column(String(500))
    image_url = Column(String(500), nullable=True)
    source = Column(String(100))
    category = Column(String(50))
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)

    # Relationships
    saved_by_users = relationship("User", secondary=user_saved_articles, back_populates="saved_articles")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ExternalServer(Base):
    __tablename__ = "external_servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    api_key = Column(String(200))
    base_url = Column(String(200))
    is_active = Column(Boolean, default=True)
    last_accessed = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200))
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")

class NotificationPreference(Base):
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String(50))
    is_enabled = Column(Boolean, default=True)
    keywords = Column(Text, nullable=True)  # Comma-separated keywords
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 