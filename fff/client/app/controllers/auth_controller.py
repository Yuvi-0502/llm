import re
from typing import Optional, Tuple
from ..services.api_client import APIClient
from ..models.user import User, UserRole, UserCredentials, UserRegistration
from .base_controller import BaseController

class AuthController(BaseController):
    def __init__(self, api_client: APIClient):
        super().__init__(api_client)

    def validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_password(self, password: str) -> bool:
        return len(password) >= 8

    def validate_username(self, username: str) -> bool:
        return 3 <= len(username) <= 50

    def get_credentials(self) -> UserCredentials:
        username = self.get_user_input("Enter username: ", self.validate_username)
        password = self.get_user_input("Enter password: ", self.validate_password)
        return UserCredentials(username=username, password=password)

    def get_registration_data(self) -> UserRegistration:
        username = self.get_user_input("Enter username: ", self.validate_username)
        email = self.get_user_input("Enter email: ", self.validate_email)
        password = self.get_user_input("Enter password: ", self.validate_password)
        return UserRegistration(username=username, email=email, password=password)

    def login(self) -> Optional[User]:
        try:
            credentials = self.get_credentials()
            response = self.api_client.login(credentials.username, credentials.password)
            user_data = self.api_client.get_user_profile()
            return User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                role=UserRole(user_data["role"]),
                is_active=user_data["is_active"],
                notify_business=user_data["notify_business"],
                notify_entertainment=user_data["notify_entertainment"],
                notify_sports=user_data["notify_sports"],
                notify_technology=user_data["notify_technology"],
                notify_keywords=user_data["notify_keywords"],
                notification_keywords=user_data["notification_keywords"]
            )
        except Exception as e:
            self.display_error(str(e))
            return None

    def signup(self) -> Optional[User]:
        try:
            registration = self.get_registration_data()
            response = self.api_client.signup(
                registration.username,
                registration.email,
                registration.password
            )
            return User(
                id=response["id"],
                username=response["username"],
                email=response["email"],
                role=UserRole(response["role"]),
                is_active=response["is_active"],
                notify_business=response["notify_business"],
                notify_entertainment=response["notify_entertainment"],
                notify_sports=response["notify_sports"],
                notify_technology=response["notify_technology"],
                notify_keywords=response["notify_keywords"],
                notification_keywords=response["notification_keywords"]
            )
        except Exception as e:
            self.display_error(str(e))
            return None

    def run(self) -> Optional[User]:
        options = ["Login", "Sign up", "Exit"]
        while True:
            choice = self.display_menu("Welcome to News Aggregator", options)
            
            if choice == 1:
                user = self.login()
                if user:
                    return user
            elif choice == 2:
                user = self.signup()
                if user:
                    return user
            elif choice == 3:
                return None 