from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List

from app.api.v1.endpoints.auth import get_current_active_user, get_current_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import User as UserSchema, UserUpdate
from app.services.email_service import EmailService

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    user_in: UserUpdate,
) -> Any:
    """
    Update current user.
    """
    if user_in.username and user_in.username != current_user.username:
        # Check if username is taken
        user = db.query(User).filter(User.username == user_in.username).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        current_user.username = user_in.username

    if user_in.email and user_in.email != current_user.email:
        # Check if email is taken
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        current_user.email = user_in.email

    if user_in.password:
        from app.core.security import get_password_hash
        current_user.hashed_password = get_password_hash(user_in.password)

    # Update notification preferences
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

@router.get("/users", response_model=List[UserSchema])
def read_users(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users. Only accessible by admin users.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/users/{user_id}/deactivate")
def deactivate_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user_id: int,
) -> Any:
    """
    Deactivate a user. Only accessible by admin users.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    user.is_active = False
    db.add(user)
    db.commit()
    return {"message": "User deactivated successfully"}

@router.post("/users/{user_id}/activate")
def activate_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user_id: int,
) -> Any:
    """
    Activate a user. Only accessible by admin users.
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    user.is_active = True
    db.add(user)
    db.commit()
    return {"message": "User activated successfully"} 