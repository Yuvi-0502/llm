from server.services.user_service import UserService
from typing import Optional

class UserController:
    def __init__(self):
        self.service = UserService()

    def get_today_headlines(self, category: Optional[str] = None, page: int = 1, limit: int = 50):
        """Get today's headlines with optional category filter and pagination"""
        return self.service.get_headlines_today(category, page, limit)

    def get_headlines_by_date_range(self, start_date: str, end_date: str, category: Optional[str] = None, 
                                   page: int = 1, limit: int = 50):
        """Get headlines for a date range with optional category filter and pagination"""
        return self.service.get_headlines_in_date_range(start_date, end_date, category, page, limit)

    def get_saved_articles(self, user_id: int, page: int = 1, limit: int = 50):
        """Get saved articles for a user with pagination"""
        return self.service.get_saved_articles(user_id, page, limit)

    def save_article(self, user_id: int, article_id: int):
        """Save an article for a user"""
        return self.service.save_article(user_id, article_id)

    def delete_article(self, user_id: int, article_id: int):
        """Delete a saved article for a user"""
        return self.service.delete_article(user_id, article_id)

    def search_articles(self, query: str, start_date: Optional[str] = None, end_date: Optional[str] = None, 
                       sort_by: str = "published_at", page: int = 1, limit: int = 50):
        """Search articles with advanced filtering and sorting"""
        return self.service.search_articles(query, start_date, end_date, sort_by, page, limit)

    def get_notifications(self, user_id: int, page: int = 1, limit: int = 50):
        """Get notifications for a user with pagination"""
        return self.service.get_user_notifications(user_id, page, limit)

    def get_article_by_id(self, article_id: int):
        """Get a specific article by ID"""
        return self.service.get_article_by_id(article_id)

    def get_categories(self):
        """Get all available categories"""
        return self.service.get_categories()

    def get_articles_by_category(self, category: str, page: int = 1, limit: int = 50):
        """Get articles by specific category with pagination"""
        return self.service.get_articles_by_category(category, page, limit)

    def logout(self, user_id: int):
        """Logout user"""
        return self.service.logout(user_id)
