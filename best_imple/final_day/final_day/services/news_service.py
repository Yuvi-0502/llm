import requests
from Repositories.news_repo import NewsRepository
from schemas.news import NewsArticleCreate
from Repositories.external_api_repo import ExternalAPIRepository
from config.constants import API_URL
from Exceptions.exceptions import ArticleNotFoundException
from config.database import DbConnection
from loguru import logger
from typing import List, Optional
from datetime import datetime
from services.notification_service import NotificationService

class NewsService:
    def __init__(self):
        self.repo = NewsRepository()
        self.external_api_repo = ExternalAPIRepository()
        self.notification_service = NotificationService()

    def get_active_api(self):
        apis = self.external_api_repo.get_api_status()
        return next((api for api in apis if api["is_active"]==1), None)

    def fetch_news(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
        return None

    def parse_articles_newsapi(self, data, server_id):
        articles = data.get("articles", [])
        parsed_articles = []
        for article in articles:
            source = article.get("source", {}).get("name")  # dict
            news = NewsArticleCreate(
                title=article.get("title"),
                server_id= server_id,
                description=article.get("description"),
                content=article.get("content"),
                source=source,
                url=article.get("url"),
                published_at=article.get("publishedAt")
            )
            parsed_articles.append(news)
        return parsed_articles

    def parse_articles_thenewsapi(self, data, server_id):
        articles = data.get("data", [])
        parsed_articles = []
        for article in articles:
            source = article.get("source")  # string
            news = NewsArticleCreate(
                title=article.get("title"),
                server_id=server_id,
                description=article.get("description"),
                content=article.get("content"),
                source=source,
                url=article.get("url"),
                published_at=article.get("published_at")
            )
            parsed_articles.append(news)
        return parsed_articles

    def store_articles(self, articles, active_api):
        for article in articles:
            self.repo.save(article)

        return{
            "message": f"{len(articles)} articles stored from {active_api['server_name']}",
            "source": active_api["server_name"]
        }

    def sync_news_from_api(self):
        logger.info("Starting sync from external API...")
        active_api = self.get_active_api()

        if not active_api:
            return {"error": "No active external APIs available"}

        active_api_url = API_URL.get(active_api["server_name"])
        active_api_server_id = active_api["server_id"]

        logger.info(f"Fetching news from {active_api_url}...")

        data = self.fetch_news(active_api_url+active_api["api_key"])

        if not data:
            return {"error": f"Failed to fetch news from {active_api['name']}"}

        if "thenewsapi" in active_api_url.lower():
            articles = self.parse_articles_thenewsapi(data,active_api_server_id)
        else:
            articles = self.parse_articles_newsapi(data,active_api_server_id)

        logger.info(f"Fetched {len(articles)} articles.")
        result = self.store_articles(articles, active_api)
        logger.success("News sync completed.")

        # Notify users for new articles
        self.notification_service.notify_users_for_articles([a.model_dump() if hasattr(a, 'model_dump') else a for a in articles])

        return result

    def get_all_articles(self, limit: int = 100) -> List[dict]:
        """Get all articles with limit"""
        return self.repo.get_all(limit)

    def get_today_articles(self) -> List[dict]:
        """Get today's articles"""
        return self.repo.get_today_articles()

    def get_articles_by_category(self, category_name: str, limit: int = 50) -> List[dict]:
        """Get articles by category"""
        return self.repo.get_by_category(category_name, limit)

    def get_article_by_id(self, article_id: int) -> dict:
        """Get specific article by ID"""
        return self.repo.get_by_id(article_id)

    def search_articles(self, query: str, start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None, category: Optional[str] = None,
                       sort_by: str = "published_at", page: int = 1, page_size: int = 10) -> List[dict]:
        """Search articles with filters"""
        return self.repo.search_articles(query, start_date, end_date, category, sort_by, page, page_size)

    def save_article(self, article_id: int, user_id: int) -> dict:
        """Save article for user"""
        # Check if article exists
        article = self.repo.get_by_id(article_id)
        if not article:
            raise ArticleNotFoundException(f"Article with ID {article_id} not found")
        
        # Save to saved_articles table
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO saved_articles (user_id, article_id) VALUES (%s, %s)",
                (user_id, article_id)
            )
            conn.commit()
            return {"message": f"Article {article_id} saved successfully"}
        except Exception as e:
            if "Duplicate entry" in str(e):
                return {"message": f"Article {article_id} is already saved"}
            raise e
        finally:
            cursor.close()
            conn.close()

    def unsave_article(self, article_id: int, user_id: int) -> dict:
        """Remove saved article for user"""
        # Check if article exists
        article = self.repo.get_by_id(article_id)
        if not article:
            raise ArticleNotFoundException(f"Article with ID {article_id} not found")
        
        # Remove from saved_articles table
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM saved_articles WHERE user_id = %s AND article_id = %s",
                (user_id, article_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                return {"message": f"Article {article_id} removed from saved list"}
            else:
                return {"message": f"Article {article_id} was not in saved list"}
        finally:
            cursor.close()
            conn.close()

    def get_saved_articles(self, user_id: int) -> List[dict]:
        """Get all saved articles for user"""
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, c.name as category_name 
            FROM articles a 
            LEFT JOIN categories c ON a.category_id = c.category_id 
            INNER JOIN saved_articles sa ON a.article_id = sa.article_id 
            WHERE sa.user_id = %s 
            ORDER BY sa.saved_at DESC
        """, (user_id,))
        articles = cursor.fetchall()
        cursor.close()
        conn.close()
        return articles

    def like_article(self, article_id: int) -> dict:
        """Like an article"""
        article = self.repo.get_by_id(article_id)
        if not article:
            raise ArticleNotFoundException(f"Article with ID {article_id} not found")
        
        current_likes = article.get('likes', 0)
        self.repo.update_likes_dislikes(article_id, current_likes + 1, article.get('dislikes', 0))
        return {"message": f"Article {article_id} liked successfully"}

    def dislike_article(self, article_id: int) -> dict:
        """Dislike an article"""
        article = self.repo.get_by_id(article_id)
        if not article:
            raise ArticleNotFoundException(f"Article with ID {article_id} not found")
        
        current_dislikes = article.get('dislikes', 0)
        self.repo.update_likes_dislikes(article_id, article.get('likes', 0), current_dislikes + 1)
        return {"message": f"Article {article_id} disliked successfully"}
