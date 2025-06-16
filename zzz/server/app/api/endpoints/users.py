from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.security import get_password_hash
from ...db.session import get_db
from ...models.user import User
from ...schemas.user import User as UserSchema, UserCreate, UserUpdate
from ..deps import get_current_active_user, get_current_admin_user

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    if user_in.username is not None:
        user = db.query(User).filter(User.username == user_in.username).first()
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        current_user.username = user_in.username
    
    if user_in.email is not None:
        user = db.query(User).filter(User.email == user_in.email).first()
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_in.email
    
    if user_in.password is not None:
        current_user.hashed_password = get_password_hash(user_in.password)
    
    if user_in.notify_business is not None:
        current_user.notify_business = user_in.notify_business
    if user_in.notify_entertainment is not None:
        current_user.notify_entertainment = user_in.notify_entertainment
    if user_in.notify_sports is not None:
        current_user.notify_sports = user_in.notify_sports
    if user_in.notify_technology is not None:
        current_user.notify_technology = user_in.notify_technology
    if user_in.notify_keywords is not None:
        current_user.notify_keywords = user_in.notify_keywords
    if user_in.notification_keywords is not None:
        current_user.notification_keywords = user_in.notification_keywords
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserSchema)
async def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 