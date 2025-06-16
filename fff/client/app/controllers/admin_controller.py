from typing import List, Optional
from ..services.api_client import APIClient
from ..models.external_api import ExternalAPI, ExternalAPIUpdate
from .base_controller import BaseController

class AdminController(BaseController):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client)

    def display_external_api(self, api: ExternalAPI):
        print("\n" + "=" * 80)
        print(f"Name: {api.name}")
        print(f"Base URL: {api.base_url}")
        print(f"API Key: {'*' * len(api.api_key)}")
        print(f"Status: {'Active' if api.is_active else 'Inactive'}")
        if api.last_accessed:
            print(f"Last Accessed: {api.last_accessed}")
        if api.description:
            print(f"Description: {api.description}")
        print("=" * 80)

    def display_external_apis(self, apis: List[ExternalAPI]):
        if not apis:
            print("\nNo external APIs found.")
            return

        for api in apis:
            self.display_external_api(api)
            print("\nOptions:")
            print("1. Update API")
            print("2. Next API")
            print("3. Back to Menu")
            
            choice = self.get_user_input("Enter your choice: ")
            if choice == "1":
                self.update_external_api(api)
            elif choice == "2":
                continue
            elif choice == "3":
                break

    def get_external_apis(self):
        try:
            apis = self.api_client.get_external_apis()
            self.display_external_apis([ExternalAPI(**api) for api in apis])
        except Exception as e:
            self.display_error(str(e))

    def update_external_api(self, api: ExternalAPI):
        print("\nUpdate External API")
        print("Leave fields empty to keep current values")
        
        name = self.get_user_input(f"Name [{api.name}]: ")
        base_url = self.get_user_input(f"Base URL [{api.base_url}]: ")
        api_key = self.get_user_input(f"API Key [{len(api.api_key) * '*'}]: ")
        description = self.get_user_input(f"Description [{api.description or ''}]: ")
        
        update_data = {}
        if name:
            update_data["name"] = name
        if base_url:
            update_data["base_url"] = base_url
        if api_key:
            update_data["api_key"] = api_key
        if description:
            update_data["description"] = description
            
        if not update_data:
            print("No changes made.")
            return
            
        try:
            updated_api = self.api_client.update_external_api(api.id, update_data)
            self.display_success("External API updated successfully")
            self.display_external_api(ExternalAPI(**updated_api))
        except Exception as e:
            self.display_error(str(e))

    def run(self):
        if not self.is_admin():
            self.display_error("Access denied. Admin privileges required.")
            return

        options = [
            "View External APIs",
            "Back to Main Menu"
        ]
        
        while True:
            choice = self.display_menu("Admin Dashboard", options)
            
            if choice == 1:
                self.get_external_apis()
            elif choice == 2:
                break 