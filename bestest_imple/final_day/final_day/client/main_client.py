from .auth_client import AuthClient
from .user_client import UserClient
from .admin_client import AdminClient

class NewsAggregatorClient(AuthClient, UserClient, AdminClient):
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        # Initialize all parent classes
        AuthClient.__init__(self, base_url)
        UserClient.__init__(self, base_url)
        AdminClient.__init__(self, base_url)

    def main_menu(self):
        """Main application menu"""
        while True:
            options = [
                "Login",
                "Sign up",
                "Exit"
            ]
            self.print_menu("NEWS AGGREGATOR", options)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                if self.login():
                    # Sync token and user_info across all client instances
                    self._sync_token_and_user_info()
                    
                    if self.user_info["role"] == "admin":
                        self.admin_menu()
                    else:
                        self.user_menu()
            elif choice == "2":
                self.register_user()
            elif choice == "3":
                print("Thank you for using News Aggregator!")
                break
            else:
                print("Invalid choice. Please try again.")

    def _sync_token_and_user_info(self):
        """Sync token and user_info across all client instances"""
        # Sync with UserClient's sub-clients
        self.news_client.token = self.token
        self.news_client.user_info = self.user_info
        self.notification_client.token = self.token
        self.notification_client.user_info = self.user_info 