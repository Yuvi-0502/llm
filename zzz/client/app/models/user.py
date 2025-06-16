from dataclasses import dataclass
from typing import Optional
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

@dataclass
class User:
    id: int
    username: str
    email: str
    role: UserRole
    is_active: bool
    notify_business: bool
    notify_entertainment: bool
    notify_sports: bool
    notify_technology: bool
    notify_keywords: bool
    notification_keywords: str

@dataclass
class UserCredentials:
    username: str
    password: str

@dataclass
class UserRegistration:
    username: str
    email: str
    password: str

@dataclass
class NotificationPreferences:
    notify_business: bool = True
    notify_entertainment: bool = True
    notify_sports: bool = True
    notify_technology: bool = True
    notify_keywords: bool = True
    notification_keywords: str = "" 