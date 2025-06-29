from server.services.news_service-1 import NewsService
from server.services.user_service import UserService
from typing import Optional

class NewsController:
    def __init__(self):
        self.news_service = NewsService()
        self.user_service = UserService()

    def fetch_news(self):
        """Fetch news from external APIs"""
        return self.news_service.fetch_news_from_api()

    def get_news_status(self):
        """Get status of news fetching and database"""
        try:
            # Get some basic statistics
            total_articles = self.user_service.repo.get_total_count()
            categories = self.user_service.get_categories()
            
            return {
                "status": "operational",
                "total_articles": total_articles,
                "categories": categories.get("categories", []),
                "message": "News aggregation system is running"
            }
        except Exception as e:
            return {"error": f"Failed to get status: {str(e)}"}

    def get_all_articles(self, page: int = 1, limit: int = 50, category: Optional[str] = None, sort_by: str = "published_at"):
        """Get all articles with pagination, filtering, and sorting"""
        try:
            offset = (page - 1) * limit
            
            # Use the user service methods for consistency
            if category:
                return self.user_service.get_articles_by_category(category, page, limit)
            else:
                # For all articles, we'll use a date range that covers everything
                from datetime import datetime, timedelta
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
                return self.user_service.get_headlines_in_date_range(start_date, end_date, None, page, limit)
        except Exception as e:
            return {"error": f"Failed to fetch articles: {str(e)}"}

    def get_article_by_id(self, article_id: int):
        """Get a specific article by ID"""
        return self.user_service.get_article_by_id(article_id)

    def get_categories(self):
        """Get all available categories"""
        return self.user_service.get_categories()

    def get_articles_by_category(self, category: str, page: int = 1, limit: int = 50):
        """Get articles by specific category"""
        return self.user_service.get_articles_by_category(category, page, limit)

    def search_articles(self, query: str, page: int = 1, limit: int = 50, 
                       category: Optional[str] = None, sort_by: str = "published_at"):
        """Search articles with advanced filtering"""
        try:
            # For now, we'll use the basic search and filter by category in the service
            # In a more advanced implementation, you might want to modify the search query
            result = self.user_service.search_articles(query, None, None, sort_by, page, limit)
            
            # Filter by category if specified
            if category and category.lower() != "all" and "articles" in result:
                filtered_articles = []
                for article in result["articles"]:
                    article_categories = article.get("categories", "")
                    if category.lower() in article_categories.lower():
                        filtered_articles.append(article)
                result["articles"] = filtered_articles
                result["search"]["category"] = category
            
            return result
        except Exception as e:
            return {"error": f"Failed to search articles: {str(e)}"}

    def get_today_articles(self, page: int = 1, limit: int = 50, category: Optional[str] = None):
        """Get today's articles with pagination and category filter"""
        return self.user_service.get_headlines_today(category, page, limit)

    def get_articles_by_date_range(self, start_date: str, end_date: str, page: int = 1, 
                                  limit: int = 50, category: Optional[str] = None):
        """Get articles for a date range with pagination and category filter"""
        return self.user_service.get_headlines_in_date_range(start_date, end_date, category, page, limit)