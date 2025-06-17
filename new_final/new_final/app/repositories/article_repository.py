from app.core.database import get_db_connection
from app.schemas.article import ArticleCreate

class ArticleRepository:
    def get(self, article_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM articles WHERE article_id = %s", (article_id,))
        article = cursor.fetchone()
        cursor.close()
        conn.close()
        return article

    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM articles")
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles

    def create(self, article: ArticleCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO articles (server_id, title, description, content, source, url, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (article.server_id, article.title, article.description, article.content, article.source, article.url, article.published_at)
        )
        conn.commit()
        cursor.close()
        conn.close()
        # Return the created article (fetch again)
        return self.get(cursor.lastrowid)

    def delete(self, article_id: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE article_id = %s", (article_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True 