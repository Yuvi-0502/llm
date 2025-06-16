from typing import Optional, Tuple
from ..models.user import User
from ..services.api_client import APIClient

class AuthController:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.current_user: Optional[User] = None

    def login(self, email: str, password: str) -> Tuple[bool, str]:
        try:
            response = self.api_client.login(email, password)
            self.current_user = User(
                id=response["user"]["id"],
                username=response["user"]["username"],
                email=response["user"]["email"],
                is_admin=response["user"]["is_admin"],
                token=response["access_token"]
            )
            self.api_client.set_token(response["access_token"])
            return True, "Login successful"
        except Exception as e:
            return False, "Invalid email or password"

    def signup(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        try:
            self.api_client.signup(username, email, password)
            return True, "Account created successfully"
        except Exception as e:
            return False, "Error creating account"

    def logout(self) -> None:
        self.current_user = None
        self.api_client.set_token(None)

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def is_admin(self) -> bool:
        return self.current_user is not None and self.current_user.is_admin 