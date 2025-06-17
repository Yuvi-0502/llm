from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, user: UserCreate):
        if self.repo.get_by_email(user.email):
            raise ValueError("Email already registered")
        return self.repo.create(user)

    def get_user_by_email(self, email: str):
        return self.repo.get_by_email(email) 