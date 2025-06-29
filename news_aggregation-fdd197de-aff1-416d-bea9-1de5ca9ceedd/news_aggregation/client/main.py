#!/usr/bin/env python3
"""
News Aggregation Client - Main Application
A console-based client for the News Aggregation System
"""

import sys
import os
from client.utils.api_client import APIClient
from client.utils.display import Display
from client.controllers.auth_controller import AuthController
from client.controllers.news_controller import NewsController
from client.controllers.admin_controller import AdminController
from client.config.config import MENU_OPTIONS


class NewsAggregationClient:
    def __init__(self):
        self.api_client = APIClient()
        self.auth_controller = AuthController(self.api_client)
        self.news_controller = NewsController(self.api_client)
        self.admin_controller = AdminController(self.api_client)
        self.running = True

    def run(self):
        """Main application loop"""
        Display.print_header("News Aggregation Client")
        
        # Check server connection
        if not self._check_server_connection():
            Display.print_error("Cannot connect to server. Please ensure the server is running.")
            return
        
        # Main application loop
        while self.running:
            if not self.auth_controller.is_logged_in():
                # Show authentication menu
                if not self.auth_controller.handle_auth_menu():
                    self.running = False
                    break
            else:
                # Show main menu based on user role
                self._show_main_menu()

    def _check_server_connection(self) -> bool:
        """Check if server is accessible"""
        Display.print_info("Checking server connection...")
        response = self.api_client.get_news_status()
        return response.get("status_code") == 200

    def _show_main_menu(self):
        """Show main menu based on user role"""
        user_role = self.auth_controller.get_user_role()
        menu_type = "admin" if user_role == "admin" else "user"
        options = MENU_OPTIONS[menu_type]
        
        Display.print_header("Main Menu")
        Display.display_user_info(self.auth_controller.get_current_user())
        Display.display_menu(options, "Main Menu")
        
        choice = Display.get_choice("Select option", list(options.keys()))
        self._handle_menu_choice(choice, menu_type)

    def _handle_menu_choice(self, choice: str, menu_type: str):
        """Handle menu choice"""
        if choice == "0":  # Exit
            self.running = False
            Display.print_info("Goodbye!")
            
        elif choice == "1":  # View Today's Headlines
            self.news_controller.view_today_headlines()
            Display.press_enter_to_continue()
            
        elif choice == "2":  # Search Articles
            self.news_controller.search_articles()
            Display.press_enter_to_continue()
            
        elif choice == "3":  # View Saved Articles
            self.news_controller.view_saved_articles()
            Display.press_enter_to_continue()
            
        elif choice == "4":  # Save Article
            self.news_controller.save_article()
            Display.press_enter_to_continue()
            
        elif choice == "5":  # View Categories
            self.news_controller.view_categories()
            Display.press_enter_to_continue()
            
        elif choice == "6":  # View Articles by Category
            self.news_controller.view_articles_by_category()
            Display.press_enter_to_continue()
            
        elif choice == "7":  # View Date Range Headlines
            self.news_controller.view_date_range_headlines()
            Display.press_enter_to_continue()
            
        elif choice == "8" and menu_type == "admin":  # Manage External Servers (Admin)
            self.admin_controller.manage_external_servers()
            Display.press_enter_to_continue()
            
        elif choice == "8" and menu_type == "user":  # Logout (User)
            self.auth_controller.logout()
            
        elif choice == "9" and menu_type == "admin":  # Create Category (Admin)
            self.admin_controller.create_category()
            Display.press_enter_to_continue()
            
        elif choice == "10" and menu_type == "admin":  # Fetch News from APIs (Admin)
            self.news_controller.fetch_news_from_apis()
            Display.press_enter_to_continue()
            
        elif choice == "11" and menu_type == "admin":  # Logout (Admin)
            self.auth_controller.logout()
            
        else:
            Display.print_error("Invalid choice")


def main():
    """Main entry point"""
    try:
        client = NewsAggregationClient()
        client.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        Display.print_error(f"Application error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 