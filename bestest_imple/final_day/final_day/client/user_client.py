from .base_client import BaseClient
from .news_client import NewsClient
from .notification_client import NotificationClient

class UserClient(BaseClient):
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        super().__init__(base_url)
        self.news_client = NewsClient(base_url)
        self.notification_client = NotificationClient(base_url)
        
        # Share token and user_info between instances
        self.news_client.token = self.token
        self.news_client.user_info = self.user_info
        self.notification_client.token = self.token
        self.notification_client.user_info = self.user_info

    def user_menu(self):
        """Regular user menu"""
        while True:
            options = [
                "Headlines",
                "Saved Articles",
                "Search",
                "Notifications",
                "Logout"
            ]
            self.print_menu("USER MENU", options)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.news_client.headlines_menu()
            elif choice == "2":
                self.news_client.saved_articles_menu()
            elif choice == "3":
                self.news_client.search_menu()
            elif choice == "4":
                self.notification_client.notifications_menu()
            elif choice == "5":
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    def _sync_token_and_user_info(self):
        """Sync token and user_info across all client instances"""
        self.news_client.token = self.token
        self.news_client.user_info = self.user_info
        self.notification_client.token = self.token
        self.notification_client.user_info = self.user_info 