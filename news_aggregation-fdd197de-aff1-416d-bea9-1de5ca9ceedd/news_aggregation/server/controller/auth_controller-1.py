from fastapi import HTTPException

from server.config.http_status_codes import HTTP_BAD_REQUEST
from server.services.authentication_service import AuthenticationService
from server.schemas.user import UserCreate
from server.schemas.auth import UserCredentials


class AuthController:
    def __init__(self):
        self.auth_service = AuthenticationService()

    def login(self, user_data: UserCredentials):
        try:
            return self.auth_service.login(user_data)
        except Exception as e:
            raise HTTPException(status_code=HTTP_BAD_REQUEST, detail=str(e))

    def register(self, user: UserCreate):
            try:
                db_user = self.auth_service.register_user(user)
                return db_user
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))