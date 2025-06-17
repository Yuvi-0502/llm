from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate):
    service = UserService()
    try:
        db_user = service.register_user(user)
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 