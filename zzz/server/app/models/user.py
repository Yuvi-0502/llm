from sqlalchemy import Column, String, Boolean, Enum
from .base import BaseModel
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Notification preferences
    notify_business = Column(Boolean, default=True)
    notify_entertainment = Column(Boolean, default=True)
    notify_sports = Column(Boolean, default=True)
    notify_technology = Column(Boolean, default=True)
    notify_keywords = Column(Boolean, default=True)
    notification_keywords = Column(String(500), default="")  # Comma-separated keywords 