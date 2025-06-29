"""
Authentication Controller for handling user authentication
"""

from typing import Dict, Any, Optional
from client.utils.api_client import APIClient
from client.utils.display import Display


class AuthController:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.current_user = None

    def login(self) -> bool:
        """Handle user login"""
        Display.print_header("User Login")
        
        email = Display.get_user_input("Enter email")
        password = Display.get_user_input("Enter password")
        
        if not email or not password:
            Display.print_error("Email and password are required")
            return False
        
        Display.print_info("Logging in...")
        response = self.api_client.login(email, password)
        
        if response.get("status_code") == 200:
            self.current_user = {
                "email": response.get("email"),
                "role": response.get("role"),
                "token": response.get("access_token")
            }
            Display.print_success("Login successful!")
            Display.display_user_info(self.current_user)
            return True
        else:
            error_msg = response.get("detail", "Login failed")
            Display.print_error(f"Login failed: {error_msg}")
            return False

    def register(self) -> bool:
        """Handle user registration"""
        Display.print_header("User Registration")
        
        username = Display.get_user_input("Enter username")
        email = Display.get_user_input("Enter email")
        password = Display.get_user_input("Enter password")
        confirm_password = Display.get_user_input("Confirm password")
        
        # Validation
        if not all([username, email, password, confirm_password]):
            Display.print_error("All fields are required")
            return False
        
        if password != confirm_password:
            Display.print_error("Passwords do not match")
            return False
        
        if len(password) < 6:
            Display.print_error("Password must be at least 6 characters long")
            return False
        
        # Ask for role (default to user)
        role_choice = Display.get_choice("Select role", ["user", "admin"])
        
        Display.print_info("Registering user...")
        response = self.api_client.register(username, email, password, role_choice)
        
        if response.get("status_code") == 200:
            Display.print_success("Registration successful! You can now login.")
            return True
        else:
            error_msg = response.get("detail", "Registration failed")
            Display.print_error(f"Registration failed: {error_msg}")
            return False

    def logout(self) -> bool:
        """Handle user logout"""
        if not self.current_user:
            Display.print_warning("No user is currently logged in")
            return True
        
        Display.print_info("Logging out...")
        response = self.api_client.logout()
        
        if response.get("status_code") == 200:
            Display.print_success("Logout successful!")
            self.current_user = None
            return True
        else:
            Display.print_warning("Logout completed (local)")
            self.current_user = None
            return True

    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current user information"""
        return self.current_user

    def get_user_role(self) -> str:
        """Get current user role"""
        return self.current_user.get("role", "user") if self.current_user else "guest"

    def show_auth_menu(self) -> str:
        """Show authentication menu and get user choice"""
        options = {
            "1": "Login",
            "2": "Register",
            "0": "Exit"
        }
        
        Display.display_menu(options, "Authentication Menu")
        return Display.get_choice("Select option", ["1", "2", "0"])

    def handle_auth_menu(self) -> bool:
        """Handle authentication menu and return True if user should continue"""
        while True:
            choice = self.show_auth_menu()
            
            if choice == "1":  # Login
                if self.login():
                    return True
                Display.press_enter_to_continue()
                
            elif choice == "2":  # Register
                self.register()
                Display.press_enter_to_continue()
                
            elif choice == "0":  # Exit
                Display.print_info("Goodbye!")
                return False 