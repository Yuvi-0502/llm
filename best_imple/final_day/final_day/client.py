import requests
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import getpass

class NewsAggregatorClient:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"
        self.token = None
        self.user_info = None

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title: str):
        """Print a formatted header"""
        print("=" * 60)
        print(f"{title:^60}")
        print("=" * 60)

    def print_menu(self, title: str, options: list):
        """Print a formatted menu"""
        self.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("=" * 60)

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to the server"""
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = response.json().get("detail", "Unknown error")
                return {"error": error_msg}
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to server. Please make sure the server is running."}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register_user(self):
        """Register a new user"""
        self.clear_screen()
        self.print_header("USER REGISTRATION")
        
        print("Please enter your details:")
        username = input("Username: ").strip()
        
        while True:
            email = input("Email: ").strip()
            if self.validate_email(email):
                break
            print("Invalid email format. Please try again.")
        
        while True:
            password = getpass.getpass("Password: ")
            if len(password) >= 6:
                break
            print("Password must be at least 6 characters long.")
        
        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            print("Passwords do not match!")
            input("Press Enter to continue...")
            return
        
        role = input("Role (admin/user) [default: user]: ").strip().lower()
        if role not in ["admin", "user"]:
            role = "user"
        
        data = {
            "user_name": username,
            "email": email,
            "password": password,
            "role": role
        }
        
        result = self.make_request("POST", "/auth/register", data)
        
        if "error" not in result:
            print("Registration successful!")
            print(f"User ID: {result.get('user_id')}")
        else:
            print(f"Registration failed: {result['error']}")
        
        input("Press Enter to continue...")

    def login(self):
        """User login"""
        self.clear_screen()
        self.print_header("USER LOGIN")
        
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ")
        
        data = {
            "email": email,
            "password": password
        }
        
        result = self.make_request("POST", "/auth/login", data)
        
        if "error" not in result:
            self.token = result["access_token"]
            self.user_info = {
                "role": result["user_role"],
                "email": email
            }
            print("Login successful!")
            return True
        else:
            print(f"Login failed: {result['error']}")
            input("Press Enter to continue...")
            return False

    def display_articles(self, articles: list, title: str = "ARTICLES"):
        """Display articles in a formatted way"""
        self.clear_screen()
        self.print_header(title)
        
        if not articles:
            print("No articles found.")
            return
        
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article.get('title', 'No title')}")
            print(f"   Source: {article.get('source', 'Unknown')}")
            print(f"   Category: {article.get('category_name', 'Uncategorized')}")
            print(f"   Published: {article.get('published_at', 'Unknown')}")
            print(f"   Likes: {article.get('likes', 0)} | Dislikes: {article.get('dislikes', 0)}")
            if article.get('description'):
                desc = article['description'][:100] + "..." if len(article['description']) > 100 else article['description']
                print(f"   Description: {desc}")
            print(f"   Article ID: {article.get('article_id')}")
            print("-" * 60)

    def headlines_menu(self):
        """Headlines submenu"""
        while True:
            options = [
                "Today",
                "Date range",
                "Back"
            ]
            self.print_menu("HEADLINES", options)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.today_headlines()
            elif choice == "2":
                self.date_range_headlines()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def today_headlines(self):
        """Show today's headlines"""
        result = self.make_request("GET", "/news/today")
        
        if "error" not in result:
            self.display_articles(result, "TODAY'S HEADLINES")
            self.article_actions_menu(result)
        else:
            print(f"Error: {result['error']}")
            input("Press Enter to continue...")

    def date_range_headlines(self):
        """Show headlines for a date range"""
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            
            # Convert to datetime for validation
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
            
            # For now, we'll use search with date range
            # In a full implementation, you'd have a specific endpoint for date range
            result = self.make_request("GET", f"/news/search?query=&start_date={start_date}&end_date={end_date}")
            
            if "error" not in result:
                self.display_articles(result, f"HEADLINES FROM {start_date} TO {end_date}")
                self.article_actions_menu(result)
            else:
                print(f"Error: {result['error']}")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
            input("Press Enter to continue...")

    def article_actions_menu(self, articles: list):
        """Menu for article actions"""
        while True:
            options = [
                "Back",
                "Logout",
                "Save Article"
            ]
            self.print_menu("ARTICLE ACTIONS", options)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                break
            elif choice == "2":
                self.logout()
                return
            elif choice == "3":
                article_id = input("Enter Article ID: ").strip()
                if article_id.isdigit():
                    result = self.make_request("POST", f"/news/{article_id}/save")
                    if "error" not in result:
                        print(result.get("message", "Article saved successfully!"))
                    else:
                        print(f"Error: {result['error']}")
                else:
                    print("Invalid Article ID")
                input("Press Enter to continue...")

    def saved_articles_menu(self):
        """Saved articles menu"""
        result = self.make_request("GET", "/news/saved/list")
        
        if "error" not in result:
            self.display_articles(result, "SAVED ARTICLES")
            
            while True:
                options = [
                    "Back",
                    "Logout",
                    "Delete Article"
                ]
                self.print_menu("SAVED ARTICLES ACTIONS", options)
                
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    break
                elif choice == "2":
                    self.logout()
                    return
                elif choice == "3":
                    article_id = input("Enter Article ID: ").strip()
                    if article_id.isdigit():
                        result = self.make_request("DELETE", f"/news/{article_id}/unsave")
                        if "error" not in result:
                            print(result.get("message", "Article removed successfully!"))
                        else:
                            print(f"Error: {result['error']}")
                    else:
                        print("Invalid Article ID")
                    input("Press Enter to continue...")
        else:
            print(f"Error: {result['error']}")
            input("Press Enter to continue...")

    def search_menu(self):
        """Search menu"""
        self.clear_screen()
        self.print_header("SEARCH ARTICLES")
        
        query = input("Enter search query: ").strip()
        if not query:
            print("Search query cannot be empty.")
            input("Press Enter to continue...")
            return
        
        # Additional search options
        use_date_range = input("Use date range? (y/n): ").strip().lower() == 'y'
        start_date = None
        end_date = None
        
        if use_date_range:
            try:
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Using current search only.")
                start_date = None
                end_date = None
        
        category = input("Category (optional): ").strip()
        if not category:
            category = None
        
        sort_by = input("Sort by (published_at/likes/dislikes) [default: published_at]: ").strip()
        if sort_by not in ["published_at", "likes", "dislikes"]:
            sort_by = "published_at"
        
        # Build search URL
        search_url = f"/news/search?query={query}&sort_by={sort_by}"
        if start_date:
            search_url += f"&start_date={start_date}"
        if end_date:
            search_url += f"&end_date={end_date}"
        if category:
            search_url += f"&category={category}"
        
        result = self.make_request("GET", search_url)
        
        if "error" not in result:
            self.display_articles(result, f"SEARCH RESULTS FOR '{query}'")
            self.article_actions_menu(result)
        else:
            print(f"Error: {result['error']}")
            input("Press Enter to continue...")

    def notifications_menu(self):
        """Notifications menu"""
        while True:
            options = [
                "View Notifications",
                "Configure Notifications",
                "Back",
                "Logout"
            ]
            self.print_menu("NOTIFICATIONS", options)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.view_notifications()
            elif choice == "2":
                self.configure_notifications()
            elif choice == "3":
                break
            elif choice == "4":
                self.logout()
                return
            else:
                print("Invalid choice. Please try again.")

    def view_notifications(self):
        """View notifications using API"""
        result = self.make_request("GET", "/notifications/")
        
        if "error" not in result:
            self.clear_screen()
            self.print_header("NOTIFICATIONS")
            
            if not result:
                print("No notifications found.")
            else:
                for i, notification in enumerate(result, 1):
                    status = "UNREAD" if not notification.get("is_read") else "READ"
                    print(f"\n{i}. [{status}] {notification.get('title', 'No title')}")
                    print(f"   {notification.get('message', 'No message')}")
                    print(f"   Date: {notification.get('created_at', 'Unknown')}")
                    print("-" * 60)
        else:
            print(f"Error: {result['error']}")
        
        input("Press Enter to continue...")

    def configure_notifications(self):
        """Configure notifications using API"""
        # First get current preferences
        result = self.make_request("GET", "/notifications/preferences")
        
        if "error" not in result:
            self.clear_screen()
            self.print_header("CONFIGURE NOTIFICATIONS")
            
            print("Current settings:")
            print(f"Email notifications: {'Enabled' if result.get('email_notifications', True) else 'Disabled'}")
            print(f"Category ID: {result.get('category_id', 'None')}")
            print(f"Keywords: {result.get('keywords', 'None')}")
            print("\n" + "=" * 60)
            
            # Get new settings
            print("\nEnter new settings (press Enter to keep current):")
            
            email_enabled = input("Enable email notifications? (y/n): ").strip().lower()
            if email_enabled in ['y', 'n']:
                email_notifications = email_enabled == 'y'
            else:
                email_notifications = result.get('email_notifications', True)
            
            category_id = input("Category ID (1-5, or press Enter for none): ").strip()
            if category_id.isdigit():
                category_id = int(category_id)
            elif category_id == "":
                category_id = result.get('category_id')
            else:
                category_id = None
            
            keywords = input("Keywords (comma-separated, or press Enter for none): ").strip()
            if keywords == "":
                keywords = result.get('keywords')
            
            # Update preferences
            update_data = {
                "email_notifications": email_notifications,
                "category_id": category_id,
                "keywords": keywords
            }
            
            update_result = self.make_request("PUT", "/notifications/preferences", update_data)
            
            if "error" not in update_result:
                print("Notification preferences updated successfully!")
            else:
                print(f"Error updating preferences: {update_result['error']}")
        else:
            print(f"Error: {result['error']}")
        
        input("Press Enter to continue...")

    def admin_menu(self):
        """Admin menu"""
        while True:
            options = [
                "View the list of external servers and status",
                "View the external server's details",
                "Update/Edit the external server's details",
                "Add new News Category",
                "Logout"
            ]
            self.print_menu("ADMIN MENU", options)
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                self.view_external_servers()
            elif choice == "2":
                self.view_external_server_details()
            elif choice == "3":
                self.update_external_server()
            elif choice == "4":
                self.add_news_category()
            elif choice == "5":
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    def view_external_servers(self):
        """View external servers status"""
        result = self.make_request("GET", "/external-servers/")
        
        if "error" not in result:
            self.clear_screen()
            self.print_header("EXTERNAL SERVERS STATUS")
            
            for server in result:
                status = "Active" if server.get("is_active") else "Not Active"
                last_accessed = server.get("last_accessed", "Never")
                print(f"{server['server_id']}. {server['server_name']} - {status}")
                print(f"   Last accessed: {last_accessed}")
                print("-" * 40)
        else:
            print(f"Error: {result['error']}")
        
        input("Press Enter to continue...")

    def view_external_server_details(self):
        """View external server details"""
        result = self.make_request("GET", "/external-servers/")
        
        if "error" not in result:
            self.clear_screen()
            self.print_header("EXTERNAL SERVER DETAILS")
            
            for server in result:
                print(f"{server['server_id']}. {server['server_name']} - {server['api_key'][:10]}...")
                print(f"   Base URL: {server['base_url']}")
                print(f"   Status: {'Active' if server.get('is_active') else 'Inactive'}")
                print("-" * 40)
        else:
            print(f"Error: {result['error']}")
        
        input("Press Enter to continue...")

    def update_external_server(self):
        """Update external server details"""
        server_id = input("Enter the external server ID: ").strip()
        
        if not server_id.isdigit():
            print("Invalid server ID")
            input("Press Enter to continue...")
            return
        
        print("Enter new values (press Enter to skip):")
        server_name = input("Server name: ").strip()
        api_key = input("API key: ").strip()
        base_url = input("Base URL: ").strip()
        is_active = input("Is active (true/false): ").strip().lower()
        
        data = {}
        if server_name:
            data["server_name"] = server_name
        if api_key:
            data["api_key"] = api_key
        if base_url:
            data["base_url"] = base_url
        if is_active in ["true", "false"]:
            data["is_active"] = is_active == "true"
        
        if data:
            result = self.make_request("PUT", f"/external-servers/{server_id}", data)
            if "error" not in result:
                print("Server updated successfully!")
            else:
                print(f"Error: {result['error']}")
        else:
            print("No changes to update")
        
        input("Press Enter to continue...")

    def add_news_category(self):
        """Add new news category via API"""
        self.clear_screen()
        self.print_header("ADD NEWS CATEGORY")
        name = input("Category name: ").strip()
        if not name:
            print("Category name cannot be empty.")
            input("Press Enter to continue...")
            return
        description = input("Description (optional): ").strip()
        data = {"name": name, "description": description}
        result = self.make_request("POST", "/categories/", data)
        if "error" not in result:
            print(f"Category '{name}' added successfully!")
        else:
            print(f"Error: {result['error']}")
        input("Press Enter to continue...")

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
                self.headlines_menu()
            elif choice == "2":
                self.saved_articles_menu()
            elif choice == "3":
                self.search_menu()
            elif choice == "4":
                self.notifications_menu()
            elif choice == "5":
                self.logout()
                break
            else:
                print("Invalid choice. Please try again.")

    def logout(self):
        """Logout user"""
        self.token = None
        self.user_info = None
        print("Logged out successfully!")

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

def main():
    """Main function"""
    client = NewsAggregatorClient()
    client.main_menu()

if __name__ == "__main__":
    main() 