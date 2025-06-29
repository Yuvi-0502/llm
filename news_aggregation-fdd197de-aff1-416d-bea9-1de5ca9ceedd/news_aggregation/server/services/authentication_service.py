from server.repos.user_repository import UserRepository
from server.schemas.auth import UserCredentials
from server.utils.password_utils import verify_password
from server.schemas.user import UserCreate
from server.core.jwt_utils import create_access_token


class AuthenticationService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, user: UserCreate):
        if self.user_repo.get_user_by_email(user.email):
            raise ValueError("Email already registered")
        return self.user_repo.create(user)

    def login(self, user_data: UserCredentials):
        user = self.user_repo.get_user_by_email(user_data.email)

        if verify_password(plain_password=user_data.password,
                           hashed_password=user['password']):
            token_payload = {
                "email": user["email"],
                "user_id": user["user_id"],
                "role": user["user_role"]
            }
            access_token = create_access_token(token_payload)
        else:
            raise ValueError("Incorrect Password")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": user["user_role"],
            "email" : user["email"]
        }


