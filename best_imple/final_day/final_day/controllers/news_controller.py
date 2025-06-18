from services.news_service import NewsService
from Exceptions.exceptions import ArticleNotFoundException
from fastapi import HTTPException
from config.http_status_code import HTTP_NOT_FOUND, HTTP_INTERNAL_SERVER_ERROR
from typing import List, Optional
from datetime import datetime

class NewsController:
    def __init__(self):
        self.news_service = NewsService()

    def fetch_news(self):
        """Fetch news from external APIs (used by scheduler)"""
        return self.news_service.sync_news_from_api()

    def get_all_articles(self, limit: int = 100) -> List[dict]:
        """Get all articles with limit"""
        try:
            return self.news_service.get_all_articles(limit)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_today_articles(self) -> List[dict]:
        """Get today's articles"""
        try:
            return self.news_service.get_today_articles()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_articles_by_category(self, category_name: str, limit: int = 50) -> List[dict]:
        """Get articles by category"""
        try:
            return self.news_service.get_articles_by_category(category_name, limit)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_article_by_id(self, article_id: int) -> dict:
        """Get specific article by ID"""
        try:
            article = self.news_service.get_article_by_id(article_id)
            if not article:
                raise ArticleNotFoundException(f"Article with ID {article_id} not found")
            return article
        except ArticleNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def search_articles(self, query: str, start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None, category: Optional[str] = None,
                       sort_by: str = "published_at", page: int = 1, page_size: int = 10) -> List[dict]:
        """Search articles with filters"""
        try:
            return self.news_service.search_articles(
                query, start_date, end_date, category, sort_by, page, page_size
            )
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def save_article(self, article_id: int, user_id: int) -> dict:
        """Save article for user"""
        try:
            return self.news_service.save_article(article_id, user_id)
        except ArticleNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def unsave_article(self, article_id: int, user_id: int) -> dict:
        """Remove saved article for user"""
        try:
            return self.news_service.unsave_article(article_id, user_id)
        except ArticleNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_saved_articles(self, user_id: int) -> List[dict]:
        """Get all saved articles for user"""
        try:
            return self.news_service.get_saved_articles(user_id)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def like_article(self, article_id: int) -> dict:
        """Like an article"""
        try:
            return self.news_service.like_article(article_id)
        except ArticleNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def dislike_article(self, article_id: int) -> dict:
        """Dislike an article"""
        try:
            return self.news_service.dislike_article(article_id)
        except ArticleNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))