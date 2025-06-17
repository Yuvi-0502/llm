from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationCreate

class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()

    def create_notification(self, notification: NotificationCreate):
        return self.repo.create(notification)

    def get_notifications_for_user(self, user_id: int):
        return self.repo.get_by_user(user_id)

    def mark_notification_as_read(self, notification_id: int):
        return self.repo.mark_as_read(notification_id) 