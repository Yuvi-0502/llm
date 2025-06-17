from client.api import APIClient
from client.auth import signup_flow, login_flow
from client.menu import main_menu, show_menu_by_role
from client.utils import clear_screen

def main():
    api = APIClient()
    while True:
        clear_screen()
        choice = main_menu()
        if choice == "1":
            if login_flow(api):
                show_menu_by_role(api)
        elif choice == "2":
            signup_flow(api)
        elif choice == "3":
            print("Exiting application.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main() 