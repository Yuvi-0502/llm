from Repositories.user_repo import UserRepository
from schemas.auth import UserCredentials
from schemas.user import UserCreate
from Utils.password_utils import verify_password
from Utils.jwt_handler import create_access_token

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, user: UserCreate):
        if self.user_repo.get_by_email(user.email):
            raise ValueError("Email already registered")
        return self.user_repo.create(user)

    def get_user_by_email(self, email: str):
        return self.user_repo.get_by_email(email)

    def login(self, user_data: UserCredentials):
        user = self.get_user_by_email(user_data.email)
        if not user:
            raise ValueError("Invalid Email")
        
        if verify_password(plain_password=user_data.password, hashed_password=user['password']):
            status = "User Logged in Successfully"
            token_payload = {
                "sub": user["email"],
                "user_id": user["user_id"],
                "role": user["role"]
            }
            access_token = create_access_token(token_payload)
        else:
            raise ValueError("Incorrect Password")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_role": user["role"]
        }

    def get_user_by_email(self, email: str):
        user = self.user_repo.get_by_email(email)
        if user is None:
            raise ValueError("Invalid Email")
        return user