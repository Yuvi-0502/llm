from .base_client import BaseClient

class NotificationClient(BaseClient):
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