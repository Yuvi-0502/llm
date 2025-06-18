from .base_client import BaseClient

class AdminClient(BaseClient):
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