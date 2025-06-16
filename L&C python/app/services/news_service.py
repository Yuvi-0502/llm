import aiohttp
import asyncio
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.models import NewsArticle, ExternalServer
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self, db: Session):
        self.db = db

    async def fetch_news_from_api(self, server: ExternalServer) -> List[dict]:
        """Fetch news from external API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    server.base_url,
                    headers={"Authorization": f"Bearer {server.api_key}"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_api_response(data, server.name)
                    else:
                        logger.error(f"Error fetching news from {server.name}: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Exception while fetching news from {server.name}: {str(e)}")
            return []

    def _process_api_response(self, data: dict, source: str) -> List[dict]:
        """Process API response based on source"""
        articles = []
        try:
            if source == "NewsAPI":
                articles = data.get("articles", [])
                return [{
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "content": article.get("content"),
                    "url": article.get("url"),
                    "image_url": article.get("urlToImage"),
                    "source": article.get("source", {}).get("name"),
                    "category": article.get("category", "general"),
                    "published_at": datetime.fromisoformat(article.get("publishedAt").replace("Z", "+00:00"))
                } for article in articles]
            elif source == "TheNewsAPI":
                articles = data.get("data", [])
                return [{
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "content": article.get("content"),
                    "url": article.get("url"),
                    "image_url": article.get("image_url"),
                    "source": article.get("source"),
                    "category": article.get("category", "general"),
                    "published_at": datetime.fromisoformat(article.get("published_at").replace("Z", "+00:00"))
                } for article in articles]
        except Exception as e:
            logger.error(f"Error processing {source} response: {str(e)}")
        return []

    async def aggregate_news(self):
        """Aggregate news from all active external servers"""
        servers = self.db.query(ExternalServer).filter(ExternalServer.is_active == True).all()
        tasks = [self.fetch_news_from_api(server) for server in servers]
        results = await asyncio.gather(*tasks)
        
        for articles in results:
            for article_data in articles:
                # Check if article already exists
                existing = self.db.query(NewsArticle).filter(
                    NewsArticle.url == article_data["url"]
                ).first()
                
                if not existing:
                    article = NewsArticle(**article_data)
                    self.db.add(article)
        
        self.db.commit()

    def get_news_by_category(self, category: str, limit: int = 10) -> List[NewsArticle]:
        """Get news articles by category"""
        return self.db.query(NewsArticle)\
            .filter(NewsArticle.category == category)\
            .order_by(NewsArticle.published_at.desc())\
            .limit(limit)\
            .all()

    def get_news_by_date_range(self, start_date: datetime, end_date: datetime) -> List[NewsArticle]:
        """Get news articles within date range"""
        return self.db.query(NewsArticle)\
            .filter(NewsArticle.published_at.between(start_date, end_date))\
            .order_by(NewsArticle.published_at.desc())\
            .all()

    def search_news(self, query: str) -> List[NewsArticle]:
        """Search news articles by query"""
        return self.db.query(NewsArticle)\
            .filter(
                (NewsArticle.title.ilike(f"%{query}%")) |
                (NewsArticle.description.ilike(f"%{query}%")) |
                (NewsArticle.content.ilike(f"%{query}%"))
            )\
            .order_by(NewsArticle.published_at.desc())\
            .all()

    def save_article_for_user(self, user_id: int, article_id: int) -> bool:
        """Save article for user"""
        try:
            article = self.db.query(NewsArticle).get(article_id)
            if article:
                article.saved_by_users.append(user_id)
                self.db.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving article for user: {str(e)}")
        return False

    def get_saved_articles(self, user_id: int) -> List[NewsArticle]:
        """Get saved articles for user"""
        return self.db.query(NewsArticle)\
            .join(NewsArticle.saved_by_users)\
            .filter(User.id == user_id)\
            .order_by(NewsArticle.published_at.desc())\
            .all() 