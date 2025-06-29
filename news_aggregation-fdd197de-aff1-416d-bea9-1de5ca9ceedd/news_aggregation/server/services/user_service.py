from server.repos.article_repo import ArticleRepository
from typing import Optional, Dict, List

class UserService:
    def __init__(self):
        self.repo = ArticleRepository()

    def get_headlines_today(self, category: Optional[str] = None, page: int = 1, limit: int = 50):
        """Get today's headlines with optional category filter and pagination"""
        try:
            offset = (page - 1) * limit
            articles = self.repo.fetch_headlines_by_day(category, limit, offset)
            total_count = self.repo.get_total_count(category)
            
            return {
                "articles": articles,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": (total_count + limit - 1) // limit
                },
                "category": category or "All"
            }
        except Exception as e:
            return {"error": f"Failed to fetch headlines: {str(e)}"}

    def get_headlines_in_date_range(self, start_date: str, end_date: str, category: Optional[str] = None, 
                                   page: int = 1, limit: int = 50):
        """Get headlines for a date range with optional category filter and pagination"""
        try:
            offset = (page - 1) * limit
            articles = self.repo.fetch_headlines_in_range(start_date, end_date, category, limit, offset)
            total_count = self.repo.get_total_count(category, start_date, end_date)
            
            return {
                "articles": articles,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": (total_count + limit - 1) // limit
                },
                "filters": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "category": category or "All"
                }
            }
        except Exception as e:
            return {"error": f"Failed to fetch headlines: {str(e)}"}

    def get_saved_articles(self, user_id: int, page: int = 1, limit: int = 50):
        """Get saved articles for a user with pagination"""
        try:
            offset = (page - 1) * limit
            articles = self.repo.fetch_saved_articles(user_id, limit, offset)
            
            return {
                "articles": articles,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": len(articles),  # Note: This is approximate
                    "pages": (len(articles) + limit - 1) // limit
                }
            }
        except Exception as e:
            return {"error": f"Failed to fetch saved articles: {str(e)}"}

    def save_article(self, user_id: int, article_id: int):
        """Save an article for a user"""
        try:
            # First check if article exists
            article = self.repo.get_article_by_id(article_id)
            if not article:
                return {"error": "Article not found", "status": "not_found"}
            
            result = self.repo.insert_saved_article(user_id, article_id)
            return result
        except Exception as e:
            return {"error": f"Failed to save article: {str(e)}"}

    def delete_article(self, user_id: int, article_id: int):
        """Delete a saved article for a user"""
        try:
            result = self.repo.remove_saved_article(user_id, article_id)
            return result
        except Exception as e:
            return {"error": f"Failed to delete article: {str(e)}"}

    def search_articles(self, query: str, start_date: Optional[str] = None, end_date: Optional[str] = None, 
                       sort_by: str = "published_at", page: int = 1, limit: int = 50):
        """Search articles with advanced filtering and sorting"""
        try:
            offset = (page - 1) * limit
            
            # Validate sort_by parameter
            valid_sort_fields = ["likes", "dislikes", "published_at"]
            if sort_by not in valid_sort_fields:
                sort_by = "published_at"
            
            articles = self.repo.search_articles(query, start_date, end_date, sort_by, limit, offset)
            
            return {
                "articles": articles,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": len(articles),  # Note: This is approximate
                    "pages": (len(articles) + limit - 1) // limit
                },
                "search": {
                    "query": query,
                    "start_date": start_date,
                    "end_date": end_date,
                    "sort_by": sort_by
                }
            }
        except Exception as e:
            return {"error": f"Failed to search articles: {str(e)}"}

    def get_user_notifications(self, user_id: int, page: int = 1, limit: int = 50):
        """Get notifications for a user with pagination"""
        try:
            offset = (page - 1) * limit
            notifications = self.repo.fetch_notifications(user_id, limit, offset)
            
            return {
                "notifications": notifications,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": len(notifications),  # Note: This is approximate
                    "pages": (len(notifications) + limit - 1) // limit
                }
            }
        except Exception as e:
            return {"error": f"Failed to fetch notifications: {str(e)}"}

    def get_article_by_id(self, article_id: int):
        """Get a specific article by ID"""
        try:
            article = self.repo.get_article_by_id(article_id)
            if not article:
                return {"error": "Article not found"}
            return {"article": article}
        except Exception as e:
            return {"error": f"Failed to fetch article: {str(e)}"}

    def get_categories(self):
        """Get all available categories"""
        try:
            categories = self.repo.get_categories()
            return {"categories": categories}
        except Exception as e:
            return {"error": f"Failed to fetch categories: {str(e)}"}

    def get_articles_by_category(self, category: str, page: int = 1, limit: int = 50):
        """Get articles by specific category with pagination"""
        try:
            offset = (page - 1) * limit
            articles = self.repo.get_articles_by_category(category, limit, offset)
            total_count = self.repo.get_total_count(category)
            
            return {
                "articles": articles,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total_count,
                    "pages": (total_count + limit - 1) // limit
                },
                "category": category
            }
        except Exception as e:
            return {"error": f"Failed to fetch articles by category: {str(e)}"}

    def logout(self, user_id: int):
        """Logout user (placeholder for future implementation)"""
        return {"message": f"User {user_id} logged out successfully."}
