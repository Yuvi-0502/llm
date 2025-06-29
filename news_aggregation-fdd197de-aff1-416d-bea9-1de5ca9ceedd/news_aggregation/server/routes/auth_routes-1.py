from fastapi import APIRouter, HTTPException

from server.schemas.auth import TokenResponse, UserCredentials
from server.schemas.user import UserCreate,UserOut
from fastapi import Depends

from server.controller.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])
auth_controller = AuthController()

@router.post("/login",response_model=TokenResponse)
def login(user_data: UserCredentials):
    try:
        return auth_controller.login(user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate):
    try:
        return auth_controller.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))