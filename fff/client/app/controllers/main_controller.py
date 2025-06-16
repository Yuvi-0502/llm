from typing import Optional
from ..services.api_client import APIClient
from ..models.user import User
from .base_controller import BaseController
from .auth_controller import AuthController
from .article_controller import ArticleController
from .admin_controller import AdminController

class MainController(BaseController):
    def __init__(self):
        self.api_client = APIClient()
        super().__init__(self.api_client)
        self.auth_controller = AuthController(self.api_client)
        self.article_controller = ArticleController(self.api_client)
        self.admin_controller = AdminController(self.api_client)

    def display_welcome(self):
        print("\n" + "=" * 80)
        print("Welcome to News Aggregation System")
        print("=" * 80)

    def get_main_menu_options(self) -> list:
        options = ["View Articles"]
        if self.current_user:
            options.extend([
                "View Saved Articles",
                "Search Articles",
                "View Articles by Date Range"
            ])
            if self.is_admin():
                options.append("Admin Dashboard")
            options.append("Logout")
        else:
            options.append("Login/Signup")
        options.append("Exit")
        return options

    def handle_main_menu_choice(self, choice: int) -> bool:
        if not self.current_user and choice > 1:
            self.display_error("Please login first")
            return True

        if choice == 1:  # View Articles
            self.article_controller.get_today_articles()
        elif choice == 2:  # View Saved Articles
            self.article_controller.get_saved_articles()
        elif choice == 3:  # Search Articles
            self.article_controller.search_articles()
        elif choice == 4:  # View Articles by Date Range
            self.article_controller.get_articles_by_date_range()
        elif choice == 5:  # Admin Dashboard or Logout
            if self.is_admin():
                self.admin_controller.run()
            else:
                self.current_user = None
                self.display_success("Logged out successfully")
        elif choice == 6:  # Login/Signup or Exit
            if not self.current_user:
                user = self.auth_controller.run()
                if user:
                    self.current_user = user
            else:
                return False
        elif choice == 7:  # Exit
            return False
        return True

    def run(self):
        self.display_welcome()
        
        while True:
            options = self.get_main_menu_options()
            choice = self.display_menu("Main Menu", options)
            
            if not self.handle_main_menu_choice(choice):
                break

        print("\nThank you for using News Aggregation System!") 