from config.database import DbConnection
from typing import Optional

class UserPreferenceRepository:
    def get_preferences(self, user_id: int) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
        pref = cursor.fetchone()
        cursor.close()
        conn.close()
        return pref

    def set_preferences(self, user_id: int, category_id: int, keywords: str, email_notifications: bool):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "REPLACE INTO user_preferences (user_id, category_id, keywords, email_notifications) VALUES (%s, %s, %s, %s)",
            (user_id, category_id, keywords, email_notifications)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def update_keywords(self, user_id: int, keywords: str):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE user_preferences SET keywords = %s WHERE user_id = %s",
            (keywords, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close() 