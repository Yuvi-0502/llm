"""
News Controller for handling news-related operations
"""

from typing import Dict, Any, Optional, List
from client.utils.api_client import APIClient
from client.utils.display import Display
from client.config.config import CATEGORIES, SORT_OPTIONS


class NewsController:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def view_today_headlines(self):
        """View today's headlines"""
        Display.print_header("Today's Headlines")
        
        # Ask for category filter
        category = self._get_category_filter()
        
        # Get articles
        response = self.api_client.get_today_headlines(category=category)
        
        if response.get("status_code") == 200:
            articles = response.get("articles", [])
            pagination = response.get("pagination", {})
            
            Display.display_articles(articles, "Today's Headlines")
            Display.display_pagination(pagination)
            
            # Show article actions
            self._show_article_actions(articles)
        else:
            error_msg = response.get("detail", "Failed to fetch headlines")
            Display.print_error(f"Error: {error_msg}")

    def search_articles(self):
        """Search articles"""
        Display.print_header("Search Articles")
        
        query = Display.get_user_input("Enter search query")
        if not query:
            Display.print_error("Search query is required")
            return
        
        # Get search filters
        start_date = Display.get_user_input("Start date (YYYY-MM-DD) [optional]")
        end_date = Display.get_user_input("End date (YYYY-MM-DD) [optional]")
        
        # Get sort option
        sort_choice = self._get_sort_option()
        
        Display.print_info("Searching articles...")
        response = self.api_client.search_articles(
            query=query,
            start_date=start_date if start_date else None,
            end_date=end_date if end_date else None,
            sort_by=sort_choice
        )
        
        if response.get("status_code") == 200:
            articles = response.get("articles", [])
            pagination = response.get("pagination", {})
            search_info = response.get("search", {})
            
            Display.display_articles(articles, f"Search Results for '{query}'")
            Display.display_pagination(pagination)
            
            # Show search info
            if search_info:
                print(f"\n{Display.COLORS['cyan']}Search: {search_info.get('query')} | Sort: {search_info.get('sort_by')}{Display.COLORS['reset']}")
            
            # Show article actions
            self._show_article_actions(articles)
        else:
            error_msg = response.get("detail", "Search failed")
            Display.print_error(f"Error: {error_msg}")

    def view_saved_articles(self):
        """View saved articles"""
        Display.print_header("Saved Articles")
        
        response = self.api_client.get_saved_articles()
        
        if response.get("status_code") == 200:
            articles = response.get("articles", [])
            pagination = response.get("pagination", {})
            
            Display.display_articles(articles, "Saved Articles")
            Display.display_pagination(pagination)
            
            # Show saved article actions
            self._show_saved_article_actions(articles)
        else:
            error_msg = response.get("detail", "Failed to fetch saved articles")
            Display.print_error(f"Error: {error_msg}")

    def save_article(self):
        """Save an article"""
        Display.print_header("Save Article")
        
        article_id = Display.get_user_input("Enter article ID to save")
        if not article_id:
            Display.print_error("Article ID is required")
            return
        
        try:
            article_id = int(article_id)
        except ValueError:
            Display.print_error("Article ID must be a number")
            return
        
        Display.print_info("Saving article...")
        response = self.api_client.save_article(article_id)
        
        if response.get("status_code") == 200:
            Display.print_success("Article saved successfully!")
        else:
            error_msg = response.get("detail", "Failed to save article")
            Display.print_error(f"Error: {error_msg}")

    def view_categories(self):
        """View available categories"""
        Display.print_header("Categories")
        
        response = self.api_client.get_categories()
        
        if response.get("status_code") == 200:
            categories = response.get("categories", [])
            Display.display_categories(categories)
        else:
            error_msg = response.get("detail", "Failed to fetch categories")
            Display.print_error(f"Error: {error_msg}")

    def view_articles_by_category(self):
        """View articles by category"""
        Display.print_header("Articles by Category")
        
        # Show available categories
        response = self.api_client.get_categories()
        if response.get("status_code") != 200:
            Display.print_error("Failed to fetch categories")
            return
        
        categories = response.get("categories", [])
        if not categories:
            Display.print_info("No categories available")
            return
        
        # Let user select category
        Display.display_categories(categories)
        category_names = [cat.get("category_name") for cat in categories]
        
        print(f"\n{Display.COLORS['yellow']}Available categories: {', '.join(category_names)}{Display.COLORS['reset']}")
        category = Display.get_user_input("Enter category name")
        
        if not category or category not in category_names:
            Display.print_error("Invalid category")
            return
        
        # Get articles for selected category
        response = self.api_client.get_articles_by_category(category)
        
        if response.get("status_code") == 200:
            articles = response.get("articles", [])
            pagination = response.get("pagination", {})
            
            Display.display_articles(articles, f"Articles in {category}")
            Display.display_pagination(pagination)
            
            # Show article actions
            self._show_article_actions(articles)
        else:
            error_msg = response.get("detail", "Failed to fetch articles")
            Display.print_error(f"Error: {error_msg}")

    def view_date_range_headlines(self):
        """View headlines for a date range"""
        Display.print_header("Date Range Headlines")
        
        start_date = Display.get_user_input("Enter start date (YYYY-MM-DD)")
        end_date = Display.get_user_input("Enter end date (YYYY-MM-DD)")
        
        if not start_date or not end_date:
            Display.print_error("Start and end dates are required")
            return
        
        # Ask for category filter
        category = self._get_category_filter()
        
        Display.print_info("Fetching articles...")
        response = self.api_client.get_headlines_by_date_range(
            start_date=start_date,
            end_date=end_date,
            category=category
        )
        
        if response.get("status_code") == 200:
            articles = response.get("articles", [])
            pagination = response.get("pagination", {})
            filters = response.get("filters", {})
            
            Display.display_articles(articles, "Date Range Headlines")
            Display.display_pagination(pagination)
            
            # Show filter info
            if filters:
                print(f"\n{Display.COLORS['cyan']}Filters: {filters.get('start_date')} to {filters.get('end_date')} | Category: {filters.get('category')}{Display.COLORS['reset']}")
            
            # Show article actions
            self._show_article_actions(articles)
        else:
            error_msg = response.get("detail", "Failed to fetch articles")
            Display.print_error(f"Error: {error_msg}")

    def fetch_news_from_apis(self):
        """Fetch news from external APIs (Admin only)"""
        Display.print_header("Fetch News from APIs")
        
        if not Display.confirm_action("This will fetch fresh news from external APIs. Continue?"):
            return
        
        Display.print_info("Fetching news from external APIs...")
        response = self.api_client.fetch_news()
        
        if response.get("status_code") == 200:
            message = response.get("message", "News fetched successfully")
            Display.print_success(message)
        else:
            error_msg = response.get("detail", "Failed to fetch news")
            Display.print_error(f"Error: {error_msg}")

    def _get_category_filter(self) -> Optional[str]:
        """Get category filter from user"""
        print(f"\n{Display.COLORS['yellow']}Available categories: {', '.join(CATEGORIES)}{Display.COLORS['reset']}")
        category = Display.get_user_input("Enter category to filter (or press Enter for all)")
        return category if category in CATEGORIES else None

    def _get_sort_option(self) -> str:
        """Get sort option from user"""
        print(f"\n{Display.COLORS['yellow']}Sort options:{Display.COLORS['reset']}")
        for key, value in SORT_OPTIONS.items():
            print(f"  {key}: {value}")
        
        sort_choice = Display.get_user_input("Enter sort option", "published_at")
        return sort_choice if sort_choice in SORT_OPTIONS else "published_at"

    def _show_article_actions(self, articles: List[Dict[str, Any]]):
        """Show actions for articles"""
        if not articles:
            return
        
        print(f"\n{Display.COLORS['green']}Article Actions:{Display.COLORS['reset']}")
        print("  save <article_id> - Save an article")
        print("  view <article_id> - View full article")
        print("  back - Return to main menu")
        
        while True:
            action = Display.get_user_input("Enter action").lower().split()
            if not action:
                continue
            
            if action[0] == "back":
                break
            elif action[0] == "save" and len(action) > 1:
                try:
                    article_id = int(action[1])
                    self._save_specific_article(article_id)
                except ValueError:
                    Display.print_error("Invalid article ID")
            elif action[0] == "view" and len(action) > 1:
                try:
                    article_id = int(action[1])
                    self._view_specific_article(article_id)
                except ValueError:
                    Display.print_error("Invalid article ID")
            else:
                Display.print_error("Invalid action")

    def _show_saved_article_actions(self, articles: List[Dict[str, Any]]):
        """Show actions for saved articles"""
        if not articles:
            return
        
        print(f"\n{Display.COLORS['green']}Saved Article Actions:{Display.COLORS['reset']}")
        print("  delete <article_id> - Remove from saved")
        print("  view <article_id> - View full article")
        print("  back - Return to main menu")
        
        while True:
            action = Display.get_user_input("Enter action").lower().split()
            if not action:
                continue
            
            if action[0] == "back":
                break
            elif action[0] == "delete" and len(action) > 1:
                try:
                    article_id = int(action[1])
                    self._delete_saved_article(article_id)
                except ValueError:
                    Display.print_error("Invalid article ID")
            elif action[0] == "view" and len(action) > 1:
                try:
                    article_id = int(action[1])
                    self._view_specific_article(article_id)
                except ValueError:
                    Display.print_error("Invalid article ID")
            else:
                Display.print_error("Invalid action")

    def _save_specific_article(self, article_id: int):
        """Save a specific article"""
        response = self.api_client.save_article(article_id)
        if response.get("status_code") == 200:
            Display.print_success(f"Article {article_id} saved successfully!")
        else:
            error_msg = response.get("detail", "Failed to save article")
            Display.print_error(f"Error: {error_msg}")

    def _delete_saved_article(self, article_id: int):
        """Delete a saved article"""
        if not Display.confirm_action(f"Remove article {article_id} from saved?"):
            return
        
        response = self.api_client.delete_saved_article(article_id)
        if response.get("status_code") == 200:
            Display.print_success(f"Article {article_id} removed from saved!")
        else:
            error_msg = response.get("detail", "Failed to remove article")
            Display.print_error(f"Error: {error_msg}")

    def _view_specific_article(self, article_id: int):
        """View a specific article"""
        response = self.api_client.get_article_by_id(article_id)
        if response.get("status_code") == 200:
            article = response.get("article")
            if article:
                Display.display_article(article)
            else:
                Display.print_error("Article not found")
        else:
            error_msg = response.get("detail", "Failed to fetch article")
            Display.print_error(f"Error: {error_msg}") 