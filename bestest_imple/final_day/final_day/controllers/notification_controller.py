from fastapi import HTTPException
from services.notification_service import NotificationService
from Repositories.notification_repo import NotificationRepository
from Repositories.user_preference_repo import UserPreferenceRepository
from config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND
from typing import List

class NotificationController:
    def __init__(self):
        self.notification_service = NotificationService()
        self.notification_repo = NotificationRepository()
        self.user_pref_repo = UserPreferenceRepository()

    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[dict]:
        """Get notifications for a specific user"""
        try:
            return self.notification_repo.get_notifications(user_id, unread_only)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def mark_notification_as_read(self, notification_id: int):
        """Mark a notification as read"""
        try:
            self.notification_repo.mark_as_read(notification_id)
            return {"message": "Notification marked as read"}
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_user_preferences(self, user_id: int) -> dict:
        """Get user notification preferences"""
        try:
            preferences = self.user_pref_repo.get_preferences(user_id)
            if not preferences:
                return {
                    "user_id": user_id,
                    "category_id": None,
                    "keywords": None,
                    "email_notifications": True
                }
            return preferences
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_user_preferences(self, user_id: int, category_id: int = None, 
                               keywords: str = None, email_notifications: bool = True) -> dict:
        """Update user notification preferences"""
        try:
            self.user_pref_repo.set_preferences(user_id, category_id, keywords, email_notifications)
            return self.get_user_preferences(user_id)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e)) 