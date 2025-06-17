from app.core.database import get_db_connection
from app.schemas.notification import NotificationCreate

class NotificationRepository:
    def get(self, notification_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notification WHERE notification_id = %s", (notification_id,))
        notification = cursor.fetchone()
        cursor.close()
        conn.close()
        return notification

    def get_by_user(self, user_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notification WHERE user_id = %s", (user_id,))
        notifications = cursor.fetchall()
        cursor.close()
        conn.close()
        return notifications

    def create(self, notification: NotificationCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO notification (user_id, message, is_read, article_id, user_enabled_keyword_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (notification.user_id, notification.message, notification.is_read, notification.article_id, notification.user_enabled_keyword_id, notification.created_at)
        )
        conn.commit()
        cursor.close()
        conn.close()
        # Return the created notification (fetch again)
        return self.get(cursor.lastrowid)

    def mark_as_read(self, notification_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notification SET is_read = TRUE WHERE notification_id = %s", (notification_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return self.get(notification_id) 