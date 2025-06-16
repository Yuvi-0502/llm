from datetime import datetime, timedelta
from typing import List, Optional
from ..services.api_client import APIClient
from ..models.article import Article, ArticleCategory, ArticleSearchParams
from .base_controller import BaseController

class ArticleController(BaseController):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client)

    def display_article(self, article: Article):
        print("\n" + "=" * 80)
        print(f"Title: {article.title}")
        if article.description:
            print(f"\nDescription: {article.description}")
        if article.author:
            print(f"\nAuthor: {article.author}")
        print(f"\nSource: {article.source_name}")
        print(f"Category: {article.category.value}")
        print(f"Published: {article.published_at}")
        print(f"Likes: {article.likes} | Dislikes: {article.dislikes}")
        if article.url:
            print(f"\nURL: {article.url}")
        print("=" * 80)

    def display_articles(self, articles: List[Article]):
        if not articles:
            print("\nNo articles found.")
            return

        for article in articles:
            self.display_article(article)
            print("\nOptions:")
            print("1. Save Article")
            print("2. Like")
            print("3. Dislike")
            print("4. Next Article")
            print("5. Back to Menu")
            
            choice = self.get_user_input("Enter your choice: ")
            if choice == "1":
                self.save_article(article.id)
            elif choice == "2":
                self.like_article(article.id)
            elif choice == "3":
                self.dislike_article(article.id)
            elif choice == "4":
                continue
            elif choice == "5":
                break

    def get_date_range(self) -> Optional[tuple[datetime, datetime]]:
        try:
            start_date_str = self.get_user_input("Enter start date (YYYY-MM-DD): ")
            end_date_str = self.get_user_input("Enter end date (YYYY-MM-DD): ")
            
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            if end_date < start_date:
                self.display_error("End date must be after start date")
                return None
                
            return start_date, end_date
        except ValueError:
            self.display_error("Invalid date format. Use YYYY-MM-DD")
            return None

    def get_category(self) -> Optional[ArticleCategory]:
        categories = [cat.value for cat in ArticleCategory]
        print("\nCategories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        
        choice = self.get_user_input("Enter category number (or press Enter for all): ")
        if not choice:
            return None
            
        try:
            return ArticleCategory(categories[int(choice) - 1])
        except (ValueError, IndexError):
            self.display_error("Invalid category")
            return None

    def get_today_articles(self):
        category = self.get_category()
        articles = self.api_client.get_today_articles(
            category.value if category else None
        )
        self.display_articles([Article(**article) for article in articles])

    def get_articles_by_date_range(self):
        date_range = self.get_date_range()
        if not date_range:
            return
            
        start_date, end_date = date_range
        category = self.get_category()
        
        articles = self.api_client.get_articles_by_date_range(
            start_date,
            end_date,
            category.value if category else None
        )
        self.display_articles([Article(**article) for article in articles])

    def search_articles(self):
        query = self.get_user_input("Enter search query: ")
        date_range = self.get_date_range()
        category = self.get_category()
        
        search_params = {
            "query": query,
            "category": category.value if category else None
        }
        
        if date_range:
            start_date, end_date = date_range
            search_params["start_date"] = start_date.isoformat()
            search_params["end_date"] = end_date.isoformat()
        
        articles = self.api_client.search_articles(search_params)
        self.display_articles([Article(**article) for article in articles])

    def get_saved_articles(self):
        articles = self.api_client.get_saved_articles()
        self.display_articles([Article(**article) for article in articles])

    def save_article(self, article_id: int):
        try:
            self.api_client.save_article(article_id)
            self.display_success("Article saved successfully")
        except Exception as e:
            self.display_error(str(e))

    def like_article(self, article_id: int):
        try:
            self.api_client.like_article(article_id)
            self.display_success("Article liked successfully")
        except Exception as e:
            self.display_error(str(e))

    def dislike_article(self, article_id: int):
        try:
            self.api_client.dislike_article(article_id)
            self.display_success("Article disliked successfully")
        except Exception as e:
            self.display_error(str(e))

    def run(self):
        options = [
            "Today's Articles",
            "Articles by Date Range",
            "Search Articles",
            "Saved Articles",
            "Back to Main Menu"
        ]
        
        while True:
            choice = self.display_menu("News Articles", options)
            
            if choice == 1:
                self.get_today_articles()
            elif choice == 2:
                self.get_articles_by_date_range()
            elif choice == 3:
                self.search_articles()
            elif choice == 4:
                self.get_saved_articles()
            elif choice == 5:
                break 