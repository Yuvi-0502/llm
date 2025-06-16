from sqlalchemy import Boolean, Column, String, Enum
from app.db.base import BaseModel
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    
    # Notification preferences
    notify_business = Column(Boolean, default=True)
    notify_entertainment = Column(Boolean, default=True)
    notify_sports = Column(Boolean, default=True)
    notify_technology = Column(Boolean, default=True)
    notify_keywords = Column(Boolean, default=True)
    notification_keywords = Column(String, nullable=True)  # Comma-separated keywords 