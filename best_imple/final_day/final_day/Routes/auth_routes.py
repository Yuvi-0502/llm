from fastapi import APIRouter, HTTPException
from schemas.auth import UserCredentials, TokenResponse
from schemas.user import UserOut, UserCreate
from controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserCredentials):
    try:
        auth_controller = AuthController()
        return auth_controller.login(user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate):
    try:
        auth_controller = AuthController()
        return auth_controller.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))