from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

# Association table for user saved articles
user_saved_articles = Table(
    'user_saved_articles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('article_id', Integer, ForeignKey('articles.id'))
)

# Association table for user notification preferences
user_notification_preferences = Table(
    'user_notification_preferences',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    saved_articles = relationship("Article", secondary=user_saved_articles, back_populates="saved_by_users")
    notification_preferences = relationship("Category", secondary=user_notification_preferences)
    keywords = relationship("UserKeyword", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    articles = relationship("Article", back_populates="category")
    users = relationship("User", secondary=user_notification_preferences)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    content = Column(Text)
    url = Column(String)
    source = Column(String)
    published_at = Column(DateTime(timezone=True))
    category_id = Column(Integer, ForeignKey("categories.id"))
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    category = relationship("Category", back_populates="articles")
    saved_by_users = relationship("User", secondary=user_saved_articles, back_populates="saved_articles")


class UserKeyword(Base):
    __tablename__ = "user_keywords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    keyword = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="keywords")


class ExternalServer(Base):
    __tablename__ = "external_servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    api_key = Column(String)
    base_url = Column(String)
    is_active = Column(Boolean, default=True)
    last_accessed = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 