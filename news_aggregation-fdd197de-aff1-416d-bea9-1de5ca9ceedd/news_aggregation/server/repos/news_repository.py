from server.core.database_connection import get_db_connection
from server.schemas.news-1 import NewsArticleCreate

class NewsRepository:
    def save(self, news: NewsArticleCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO articles (server_id, title, description, content, source, url, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                news.server_id,
                news.title,
                news.description,
                news.content,
                news.source,
                news.url,
                news.published_at
            )
        )
        conn.commit()
        article_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return article_id

    def find_latest_article_id(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT article_id FROM articles ORDER BY article_id DESC LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
