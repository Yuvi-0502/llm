from server.core.database_connection import get_db_connection

class SavedArticleRepository:
    def get_by_user(self, user_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT a.* FROM saved_articles s JOIN article a ON s.article_id = a.article_id WHERE s.user_id = %s", (user_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
