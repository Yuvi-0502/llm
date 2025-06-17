from client.api import APIClient
from client.utils import clear_screen, pause

def main_menu():
    print("\nWelcome to the News Aggregator application. Please choose the options below.")
    print("1. Login")
    print("2. Sign up")
    print("3. Exit")
    return input("Enter your choice: ")

def admin_menu(api: APIClient):
    while True:
        clear_screen()
        print("\nAdmin Menu:")
        print("1. View external servers and status")
        print("2. View external server details")
        print("3. Update/Edit external server API key")
        print("4. Add new News Category")
        print("5. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            resp = api.get_external_servers()
            if resp.ok:
                for srv in resp.json():
                    print(f"{srv['server_id']}: {srv['server_name']} - {'Active' if srv['is_active'] else 'Not Active'} - last accessed: {srv.get('last_accessed')}")
            else:
                print("Failed to fetch servers.")
            pause()
        elif choice == "2":
            server_id = input("Enter server ID: ")
            resp = api.get_external_server_details(server_id)
            if resp.ok:
                srv = resp.json()
                print(f"Server: {srv['server_name']} - API Key: {srv['api_key']}")
            else:
                print("Failed to fetch server details.")
            pause()
        elif choice == "3":
            server_id = input("Enter server ID: ")
            api_key = input("Enter new API key: ")
            resp = api.update_external_server_api_key(server_id, api_key)
            if resp.ok:
                print("API key updated.")
            else:
                print("Failed to update API key.")
            pause()
        elif choice == "4":
            category_name = input("Enter new category name: ")
            resp = api.add_category(category_name)
            if resp.ok:
                print("Category added.")
            else:
                print("Failed to add category.")
            pause()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")
            pause()

def user_menu(api: APIClient):
    while True:
        clear_screen()
        print("\nUser Menu:")
        print("1. View Headlines")
        print("2. View Categories")
        print("3. Save Article")
        print("4. View Saved Articles")
        print("5. Delete Saved Article")
        print("6. Search Articles")
        print("7. Notifications")
        print("8. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            resp = api.get_articles()
            if resp.ok:
                for art in resp.json():
                    print(f"{art['article_id']}: {art['title']}")
            else:
                print("Failed to fetch articles.")
            pause()
        elif choice == "2":
            resp = api.get_categories()
            if resp.ok:
                for cat in resp.json():
                    print(f"{cat['category_id']}: {cat['category_name']}")
            else:
                print("Failed to fetch categories.")
            pause()
        elif choice == "3":
            article_id = input("Enter Article ID to save: ")
            resp = api.save_article(article_id)
            if resp.ok:
                print("Article saved.")
            else:
                print("Failed to save article.")
            pause()
        elif choice == "4":
            resp = api.get_saved_articles()
            if resp.ok:
                for art in resp.json():
                    print(f"{art['saved_id']}: {art['article_id']}")
            else:
                print("Failed to fetch saved articles.")
            pause()
        elif choice == "5":
            saved_id = input("Enter Saved Article ID to delete: ")
            resp = api.delete_saved_article(saved_id)
            if resp.ok:
                print("Saved article deleted.")
            else:
                print("Failed to delete saved article.")
            pause()
        elif choice == "6":
            query = input("Enter search query: ")
            start_date = input("Start date (YYYY-MM-DD, optional): ")
            end_date = input("End date (YYYY-MM-DD, optional): ")
            resp = api.search_articles(query, start_date or None, end_date or None)
            if resp.ok:
                for art in resp.json():
                    print(f"{art['article_id']}: {art['title']}")
            else:
                print("Search failed.")
            pause()
        elif choice == "7":
            notification_menu(api)
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")
            pause()

def notification_menu(api: APIClient):
    while True:
        clear_screen()
        print("\nNotifications Menu:")
        print("1. View Notifications")
        print("2. Configure Notifications (stub)")
        print("3. Add Keyword (stub)")
        print("4. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            resp = api.get_notifications()
            if resp.ok:
                for n in resp.json():
                    print(f"{n['notification_id']}: {n['message']}")
            else:
                print("Failed to fetch notifications.")
            pause()
        elif choice == "2":
            print("Notification configuration not implemented in demo.")
            pause()
        elif choice == "3":
            print("Keyword addition not implemented in demo.")
            pause()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
            pause()

def show_menu_by_role(api: APIClient):
    if api.user_role == "admin":
        admin_menu(api)
    else:
        user_menu(api) 