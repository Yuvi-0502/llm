from config.database import DbConnection
from schemas.news import NewsArticleCreate, NewsArticleUpdate
from datetime import datetime, timedelta
from typing import List, Optional

class NewsRepository:
    def save(self, article: NewsArticleCreate):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO articles (title, description, content, url, source, published_at, server_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            article.title, article.description, article.content, 
            article.url, article.source, article.published_at, article.server_id
        ))
        
        conn.commit()
        article_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return article_id

    def get_all(self, limit: int = 100):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, c.name as category_name 
            FROM articles a 
            LEFT JOIN categories c ON a.category_id = c.category_id 
            ORDER BY a.published_at DESC 
            LIMIT %s
        """, (limit,))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles

    def get_by_id(self, article_id: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, c.name as category_name 
            FROM articles a 
            LEFT JOIN categories c ON a.category_id = c.category_id 
            WHERE a.article_id = %s
        """, (article_id,))
        article = cursor.fetchone()
        cursor.close()
        conn.close()
        return article

    def get_by_category(self, category_name: str, limit: int = 50):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, c.name as category_name 
            FROM articles a 
            LEFT JOIN categories c ON a.category_id = c.category_id 
            WHERE c.name = %s 
            ORDER BY a.published_at DESC 
            LIMIT %s
        """, (category_name, limit))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles

    def get_today_articles(self):
        today = datetime.now().date()
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, c.name as category_name 
            FROM articles a 
            LEFT JOIN categories c ON a.category_id = c.category_id 
            WHERE DATE(a.published_at) = %s 
            ORDER BY a.published_at DESC
        """, (today,))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles

    def search_articles(self, query: str, start_date: Optional[datetime] = None, 
                       end_date: Optional[datetime] = None, category: Optional[str] = None,
                       sort_by: str = "published_at", page: int = 1, page_size: int = 10):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Build the query
        sql = """
            SELECT a.*, c.name as category_name 
            FROM articles a 
            LEFT JOIN categories c ON a.category_id = c.category_id 
            WHERE (a.title LIKE %s OR a.description LIKE %s OR a.content LIKE %s)
        """
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        
        if start_date:
            sql += " AND a.published_at >= %s"
            params.append(start_date)
        
        if end_date:
            sql += " AND a.published_at <= %s"
            params.append(end_date)
        
        if category:
            sql += " AND c.name = %s"
            params.append(category)
        
        # Add sorting
        if sort_by == "likes":
            sql += " ORDER BY a.likes DESC"
        elif sort_by == "dislikes":
            sql += " ORDER BY a.dislikes DESC"
        else:
            sql += " ORDER BY a.published_at DESC"
        
        # Add pagination
        offset = (page - 1) * page_size
        sql += " LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        
        cursor.execute(sql, params)
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles

    def update_category(self, article_id: int, category_id: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE articles SET category_id = %s WHERE article_id = %s",
            (category_id, article_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def update_likes_dislikes(self, article_id: int, likes: int = 0, dislikes: int = 0):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE articles SET likes = %s, dislikes = %s WHERE article_id = %s",
            (likes, dislikes, article_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def get_articles_by_date_range(self, start_date: datetime, end_date: datetime):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, c.name as category_name 
            FROM articles a 
            LEFT JOIN categories c ON a.category_id = c.category_id 
            WHERE a.published_at BETWEEN %s AND %s 
            ORDER BY a.published_at DESC
        """, (start_date, end_date))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles