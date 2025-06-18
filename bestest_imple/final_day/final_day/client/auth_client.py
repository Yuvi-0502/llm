import getpass
from .base_client import BaseClient

class AuthClient(BaseClient):
    def register_user(self):
        """Register a new user"""
        self.clear_screen()
        self.print_header("USER REGISTRATION")
        
        print("Please enter your details:")
        username = input("Username: ").strip()
        
        while True:
            email = input("Email: ").strip()
            if self.validate_email(email):
                break
            print("Invalid email format. Please try again.")
        
        while True:
            password = getpass.getpass("Password: ")
            if len(password) >= 6:
                break
            print("Password must be at least 6 characters long.")
        
        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            print("Passwords do not match!")
            input("Press Enter to continue...")
            return
        
        role = input("Role (admin/user) [default: user]: ").strip().lower()
        if role not in ["admin", "user"]:
            role = "user"
        
        data = {
            "user_name": username,
            "email": email,
            "password": password,
            "role": role
        }
        
        result = self.make_request("POST", "/auth/register", data)
        
        if "error" not in result:
            print("Registration successful!")
            print(f"User ID: {result.get('user_id')}")
        else:
            print(f"Registration failed: {result['error']}")
        
        input("Press Enter to continue...")

    def login(self):
        """User login"""
        self.clear_screen()
        self.print_header("USER LOGIN")
        
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ")
        
        data = {
            "email": email,
            "password": password
        }
        
        result = self.make_request("POST", "/auth/login", data)
        
        if "error" not in result:
            self.token = result["access_token"]
            self.user_info = {
                "role": result["user_role"],
                "email": email
            }
            print("Login successful!")
            return True
        else:
            print(f"Login failed: {result['error']}")
            input("Press Enter to continue...")
            return False 