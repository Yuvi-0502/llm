from config.database import DbConnection
from datetime import datetime
from typing import List, Optional

class NotificationRepository:
    def add_notification(self, user_id: int, title: str, message: str):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notifications (user_id, title, message, is_read, created_at) VALUES (%s, %s, %s, %s, %s)",
            (user_id, title, message, False, datetime.now())
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_notifications(self, user_id: int, unread_only: bool = False) -> List[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM notifications WHERE user_id = %s"
        params = [user_id]
        if unread_only:
            sql += " AND is_read = FALSE"
        sql += " ORDER BY created_at DESC"
        cursor.execute(sql, params)
        notifications = cursor.fetchall()
        cursor.close()
        conn.close()
        return notifications

    def mark_as_read(self, notification_id: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notifications SET is_read = TRUE WHERE notification_id = %s",
            (notification_id,)
        )
        conn.commit()
        cursor.close()
        conn.close() 