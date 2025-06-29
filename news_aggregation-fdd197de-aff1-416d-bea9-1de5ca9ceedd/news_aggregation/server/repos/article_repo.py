from server.core.database_connection import get_db_connection
from typing import List, Dict, Optional
from datetime import datetime

class ArticleRepository:
    def fetch_headlines_by_day(self, category: Optional[str] = None, limit: int = 50, offset: int = 0):
        """Fetch headlines for today with optional category filter and pagination"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if category and category.lower() != "all":
            # Join with category mapping to filter by category
            sql = """
                SELECT DISTINCT a.*, c.category_name 
                FROM articles a
                JOIN article_category_mapping acm ON a.article_id = acm.article_id
                JOIN category c ON acm.category_id = c.category_id
                WHERE DATE(a.published_at) = CURDATE() 
                AND c.category_name = %s
                ORDER BY a.published_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (category, limit, offset))
        else:
            # Get all articles for today
            sql = """
                SELECT a.*, GROUP_CONCAT(c.category_name) as categories
                FROM articles a
                LEFT JOIN article_category_mapping acm ON a.article_id = acm.article_id
                LEFT JOIN category c ON acm.category_id = c.category_id
                WHERE DATE(a.published_at) = CURDATE()
                GROUP BY a.article_id
                ORDER BY a.published_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (limit, offset))
        
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def fetch_headlines_in_range(self, start_date: str, end_date: str, category: Optional[str] = None, limit: int = 50, offset: int = 0):
        """Fetch headlines for a date range with optional category filter and pagination"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if category and category.lower() != "all":
            # Join with category mapping to filter by category
            sql = """
                SELECT DISTINCT a.*, c.category_name 
                FROM articles a
                JOIN article_category_mapping acm ON a.article_id = acm.article_id
                JOIN category c ON acm.category_id = c.category_id
                WHERE a.published_at BETWEEN %s AND %s 
                AND c.category_name = %s
                ORDER BY a.published_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (start_date, end_date, category, limit, offset))
        else:
            # Get all articles in date range
            sql = """
                SELECT a.*, GROUP_CONCAT(c.category_name) as categories
                FROM articles a
                LEFT JOIN article_category_mapping acm ON a.article_id = acm.article_id
                LEFT JOIN category c ON acm.category_id = c.category_id
                WHERE a.published_at BETWEEN %s AND %s
                GROUP BY a.article_id
                ORDER BY a.published_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (start_date, end_date, limit, offset))
        
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def fetch_saved_articles(self, user_id: int, limit: int = 50, offset: int = 0):
        """Fetch saved articles for a user with pagination"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT a.*, sa.saved_at, GROUP_CONCAT(c.category_name) as categories
            FROM saved_article sa
            JOIN articles a ON sa.article_id = a.article_id
            LEFT JOIN article_category_mapping acm ON a.article_id = acm.article_id
            LEFT JOIN category c ON acm.category_id = c.category_id
            WHERE sa.user_id = %s
            GROUP BY a.article_id
            ORDER BY sa.saved_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (user_id, limit, offset))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def insert_saved_article(self, user_id: int, article_id: int):
        """Save an article for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if article is already saved
        cursor.execute("SELECT * FROM saved_article WHERE user_id = %s AND article_id = %s", (user_id, article_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {"message": "Article already saved", "status": "exists"}
        
        cursor.execute("INSERT INTO saved_article (user_id, article_id) VALUES (%s, %s)", (user_id, article_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Article saved successfully", "status": "saved"}

    def remove_saved_article(self, user_id: int, article_id: int):
        """Remove a saved article for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM saved_article WHERE user_id = %s AND article_id = %s", (user_id, article_id))
        affected_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        
        if affected_rows > 0:
            return {"message": "Article removed from saved list", "status": "removed"}
        else:
            return {"message": "Article not found in saved list", "status": "not_found"}

    def search_articles(self, query: str, start_date: Optional[str] = None, end_date: Optional[str] = None, 
                       sort_by: str = "published_at", limit: int = 50, offset: int = 0):
        """Search articles with advanced filtering and sorting"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Build the base query
        sql = """
            SELECT a.*, GROUP_CONCAT(c.category_name) as categories
            FROM articles a
            LEFT JOIN article_category_mapping acm ON a.article_id = acm.article_id
            LEFT JOIN category c ON acm.category_id = c.category_id
            WHERE (a.title LIKE %s OR a.description LIKE %s OR a.content LIKE %s)
        """
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        
        # Add date range filter
        if start_date and end_date:
            sql += " AND a.published_at BETWEEN %s AND %s"
            params += [start_date, end_date]
        
        # Group by article and add sorting
        sql += " GROUP BY a.article_id"
        
        # Add sorting
        if sort_by in ["likes", "dislikes", "published_at"]:
            sql += f" ORDER BY a.{sort_by} DESC"
        else:
            sql += " ORDER BY a.published_at DESC"
        
        # Add pagination
        sql += " LIMIT %s OFFSET %s"
        params += [limit, offset]
        
        cursor.execute(sql, tuple(params))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def fetch_notifications(self, user_id: int, limit: int = 50, offset: int = 0):
        """Fetch notifications for a user with pagination"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT n.*, a.title as article_title, a.url as article_url
            FROM notification n
            LEFT JOIN articles a ON n.article_id = a.article_id
            WHERE n.user_id = %s
            ORDER BY n.notification_id DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (user_id, limit, offset))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def get_article_by_id(self, article_id: int):
        """Get a specific article by ID with categories"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT a.*, GROUP_CONCAT(c.category_name) as categories
            FROM articles a
            LEFT JOIN article_category_mapping acm ON a.article_id = acm.article_id
            LEFT JOIN category c ON acm.category_id = c.category_id
            WHERE a.article_id = %s
            GROUP BY a.article_id
        """
        cursor.execute(sql, (article_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def get_categories(self):
        """Get all available categories"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category ORDER BY category_name")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def get_articles_by_category(self, category: str, limit: int = 50, offset: int = 0):
        """Get articles by specific category"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT DISTINCT a.*, c.category_name
            FROM articles a
            JOIN article_category_mapping acm ON a.article_id = acm.article_id
            JOIN category c ON acm.category_id = c.category_id
            WHERE c.category_name = %s
            ORDER BY a.published_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (category, limit, offset))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def get_total_count(self, category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Get total count of articles for pagination"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if category and category.lower() != "all":
            sql = """
                SELECT COUNT(DISTINCT a.article_id) as total
                FROM articles a
                JOIN article_category_mapping acm ON a.article_id = acm.article_id
                JOIN category c ON acm.category_id = c.category_id
                WHERE c.category_name = %s
            """
            params = [category]
        else:
            sql = "SELECT COUNT(*) as total FROM articles a WHERE 1=1"
            params = []
        
        if start_date and end_date:
            sql += " AND a.published_at BETWEEN %s AND %s"
            params += [start_date, end_date]
        
        cursor.execute(sql, tuple(params))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else 0
