from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import User, NotificationPreference
from app.schemas.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user_data: UserCreate) -> Optional[User]:
        """Create new user"""
        try:
            # Check if user already exists
            if self.get_user_by_email(user_data.email) or self.get_user_by_username(user_data.username):
                return None

            # Create new user
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password,
                is_admin=False
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)

            # Create default notification preferences
            self._create_default_notification_preferences(db_user.id)

            return db_user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            self.db.rollback()
            return None

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        try:
            user = self.db.query(User).get(user_id)
            if not user:
                return None

            update_data = user_data.dict(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

            for key, value in update_data.items():
                setattr(user, key, value)

            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            self.db.rollback()
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def _create_default_notification_preferences(self, user_id: int):
        """Create default notification preferences for new user"""
        default_categories = ["business", "entertainment", "sports", "technology"]
        for category in default_categories:
            preference = NotificationPreference(
                user_id=user_id,
                category=category,
                is_enabled=True
            )
            self.db.add(preference)
        self.db.commit()

    def get_notification_preferences(self, user_id: int) -> list:
        """Get user's notification preferences"""
        return self.db.query(NotificationPreference)\
            .filter(NotificationPreference.user_id == user_id)\
            .all()

    def update_notification_preference(self, user_id: int, category: str, is_enabled: bool, keywords: Optional[str] = None) -> bool:
        """Update user's notification preference"""
        try:
            preference = self.db.query(NotificationPreference)\
                .filter(
                    NotificationPreference.user_id == user_id,
                    NotificationPreference.category == category
                ).first()

            if preference:
                preference.is_enabled = is_enabled
                if keywords is not None:
                    preference.keywords = keywords
                self.db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating notification preference: {str(e)}")
            self.db.rollback()
            return False 