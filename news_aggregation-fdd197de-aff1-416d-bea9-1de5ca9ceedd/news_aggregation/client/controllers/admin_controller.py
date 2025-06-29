"""
Admin Controller for handling admin-specific operations
"""

from typing import Dict, Any, List
from client.utils.api_client import APIClient
from client.utils.display import Display


class AdminController:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def manage_external_servers(self):
        """Manage external servers"""
        Display.print_header("Manage External Servers")
        
        response = self.api_client.get_external_servers()
        
        if response.get("status_code") == 200:
            servers = response.get("servers", [])
            Display.display_external_servers(servers)
            
            if servers:
                self._show_server_actions(servers)
        else:
            error_msg = response.get("detail", "Failed to fetch external servers")
            Display.print_error(f"Error: {error_msg}")

    def create_category(self):
        """Create a new category"""
        Display.print_header("Create Category")
        
        category_name = Display.get_user_input("Enter category name")
        if not category_name:
            Display.print_error("Category name is required")
            return
        
        # Validate category name
        if len(category_name) < 2:
            Display.print_error("Category name must be at least 2 characters long")
            return
        
        if not category_name.replace(" ", "").isalnum():
            Display.print_error("Category name can only contain letters, numbers, and spaces")
            return
        
        Display.print_info("Creating category...")
        response = self.api_client.create_category(category_name)
        
        if response.get("status_code") == 200:
            Display.print_success(f"Category '{category_name}' created successfully!")
        else:
            error_msg = response.get("detail", "Failed to create category")
            Display.print_error(f"Error: {error_msg}")

    def _show_server_actions(self, servers: List[Dict[str, Any]]):
        """Show actions for external servers"""
        print(f"\n{Display.COLORS['green']}Server Actions:{Display.COLORS['reset']}")
        print("  update <server_id> - Update server API key")
        print("  back - Return to main menu")
        
        while True:
            action = Display.get_user_input("Enter action").lower().split()
            if not action:
                continue
            
            if action[0] == "back":
                break
            elif action[0] == "update" and len(action) > 1:
                try:
                    server_id = int(action[1])
                    self._update_server_api_key(server_id)
                except ValueError:
                    Display.print_error("Invalid server ID")
            else:
                Display.print_error("Invalid action")

    def _update_server_api_key(self, server_id: int):
        """Update server API key"""
        Display.print_header(f"Update Server {server_id}")
        
        new_api_key = Display.get_user_input("Enter new API key")
        if not new_api_key:
            Display.print_error("API key is required")
            return
        
        if not Display.confirm_action(f"Update API key for server {server_id}?"):
            return
        
        Display.print_info("Updating server...")
        response = self.api_client.update_external_server(server_id, new_api_key)
        
        if response.get("status_code") == 200:
            Display.print_success(f"Server {server_id} updated successfully!")
        else:
            error_msg = response.get("detail", "Failed to update server")
            Display.print_error(f"Error: {error_msg}") 