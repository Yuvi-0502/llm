"""
Display utilities for console output formatting
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from client.config.config import COLORS, DISPLAY_SETTINGS


class Display:
    @staticmethod
    def clear_screen():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title: str):
        """Print a formatted header"""
        print(f"\n{COLORS['cyan']}{'='*60}")
        print(f"{COLORS['bold']}{title.center(60)}")
        print(f"{COLORS['cyan']}{'='*60}{COLORS['reset']}")

    @staticmethod
    def print_subheader(title: str):
        """Print a formatted subheader"""
        print(f"\n{COLORS['blue']}{'-'*40}")
        print(f"{COLORS['bold']}{title}")
        print(f"{COLORS['blue']}{'-'*40}{COLORS['reset']}")

    @staticmethod
    def print_success(message: str):
        """Print a success message"""
        print(f"{COLORS['green']}✓ {message}{COLORS['reset']}")

    @staticmethod
    def print_error(message: str):
        """Print an error message"""
        print(f"{COLORS['red']}✗ {message}{COLORS['reset']}")

    @staticmethod
    def print_warning(message: str):
        """Print a warning message"""
        print(f"{COLORS['yellow']}⚠ {message}{COLORS['reset']}")

    @staticmethod
    def print_info(message: str):
        """Print an info message"""
        print(f"{COLORS['blue']}ℹ {message}{COLORS['reset']}")

    @staticmethod
    def truncate_text(text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if not text:
            return ""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

    @staticmethod
    def format_date(date_string: str) -> str:
        """Format date string for display"""
        try:
            if date_string:
                # Handle different date formats
                if 'T' in date_string:
                    # ISO format: 2024-01-15T10:30:00
                    dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
                else:
                    # Simple format: 2024-01-15
                    dt = datetime.strptime(date_string, "%Y-%m-%d")
                return dt.strftime(DISPLAY_SETTINGS["date_format"])
        except:
            pass
        return date_string or "Unknown"

    @staticmethod
    def display_article(article: Dict[str, Any], index: Optional[int] = None):
        """Display a single article"""
        title = Display.truncate_text(article.get('title', 'No Title'), 
                                     DISPLAY_SETTINGS["max_title_length"])
        description = Display.truncate_text(article.get('description', 'No description'), 
                                          DISPLAY_SETTINGS["max_description_length"])
        source = article.get('source', 'Unknown Source')
        published_at = Display.format_date(article.get('published_at', ''))
        article_id = article.get('article_id', 'N/A')
        likes = article.get('likes', 0)
        dislikes = article.get('dislikes', 0)
        categories = article.get('categories', '')

        # Print article with index if provided
        index_str = f"{index}. " if index is not None else ""
        
        print(f"\n{COLORS['bold']}{index_str}{title}{COLORS['reset']}")
        print(f"{COLORS['yellow']}Source: {source} | Published: {published_at}{COLORS['reset']}")
        print(f"{COLORS['cyan']}ID: {article_id} | 👍 {likes} | 👎 {dislikes}{COLORS['reset']}")
        if categories:
            print(f"{COLORS['magenta']}Categories: {categories}{COLORS['reset']}")
        print(f"{description}")
        if article.get('url'):
            print(f"{COLORS['blue']}URL: {article.get('url')}{COLORS['reset']}")

    @staticmethod
    def display_articles(articles: List[Dict[str, Any]], title: str = "Articles"):
        """Display a list of articles"""
        if not articles:
            Display.print_info("No articles found.")
            return

        Display.print_subheader(f"{title} ({len(articles)} found)")
        
        for i, article in enumerate(articles, 1):
            Display.display_article(article, i)

    @staticmethod
    def display_pagination(pagination: Dict[str, Any]):
        """Display pagination information"""
        if not pagination:
            return
            
        page = pagination.get('page', 1)
        total_pages = pagination.get('pages', 1)
        total_items = pagination.get('total', 0)
        limit = pagination.get('limit', 10)

        print(f"\n{COLORS['cyan']}Page {page} of {total_pages} | Total: {total_items} items | Per page: {limit}{COLORS['reset']}")

    @staticmethod
    def display_menu(options: Dict[str, str], title: str = "Menu"):
        """Display a menu with options"""
        Display.print_subheader(title)
        for key, value in options.items():
            print(f"{COLORS['yellow']}{key}{COLORS['reset']}. {value}")

    @staticmethod
    def display_categories(categories: List[Dict[str, Any]]):
        """Display categories"""
        if not categories:
            Display.print_info("No categories found.")
            return

        Display.print_subheader("Available Categories")
        for i, category in enumerate(categories, 1):
            name = category.get('category_name', 'Unknown')
            print(f"{COLORS['yellow']}{i}{COLORS['reset']}. {name}")

    @staticmethod
    def display_external_servers(servers: List[Dict[str, Any]]):
        """Display external servers"""
        if not servers:
            Display.print_info("No external servers found.")
            return

        Display.print_subheader("External Servers")
        for server in servers:
            server_id = server.get('server_id', 'N/A')
            name = server.get('server_name', 'Unknown')
            is_active = server.get('is_active', False)
            status = f"{COLORS['green']}Active{COLORS['reset']}" if is_active else f"{COLORS['red']}Inactive{COLORS['reset']}"
            
            print(f"{COLORS['yellow']}ID: {server_id}{COLORS['reset']} | {name} | Status: {status}")

    @staticmethod
    def display_user_info(user_data: Dict[str, Any]):
        """Display user information"""
        Display.print_subheader("User Information")
        print(f"{COLORS['yellow']}Email: {COLORS['reset']}{user_data.get('email', 'N/A')}")
        print(f"{COLORS['yellow']}Username: {COLORS['reset']}{user_data.get('username', 'N/A')}")
        print(f"{COLORS['yellow']}Role: {COLORS['reset']}{user_data.get('role', 'N/A')}")

    @staticmethod
    def get_user_input(prompt: str, default: str = "") -> str:
        """Get user input with optional default value"""
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()

    @staticmethod
    def get_choice(prompt: str, valid_choices: List[str]) -> str:
        """Get user choice from valid options"""
        while True:
            choice = Display.get_user_input(prompt).lower()
            if choice in valid_choices:
                return choice
            Display.print_error(f"Invalid choice. Please choose from: {', '.join(valid_choices)}")

    @staticmethod
    def confirm_action(prompt: str = "Are you sure?") -> bool:
        """Get user confirmation for an action"""
        while True:
            response = Display.get_user_input(f"{prompt} (y/n)").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            Display.print_error("Please enter 'y' or 'n'")

    @staticmethod
    def press_enter_to_continue():
        """Wait for user to press Enter"""
        input(f"\n{COLORS['cyan']}Press Enter to continue...{COLORS['reset']}") 