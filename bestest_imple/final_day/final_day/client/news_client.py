from datetime import datetime
from .base_client import BaseClient

class NewsClient(BaseClient):
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