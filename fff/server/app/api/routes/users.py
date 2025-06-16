from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.container import Container, get_container
from app.core.security import get_current_user, get_current_admin_user
from app.schemas.user import User, UserUpdate, NotificationPreferencesUpdate

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """Get current user."""
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container)
):
    """Update current user."""
    updated_user = container.user_service.update_user(
        user_id=current_user.id,
        user=user_update
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.put("/me/notifications", response_model=User)
async def update_notification_preferences(
    preferences: NotificationPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container)
):
    """Update current user's notification preferences."""
    updated_user = container.user_service.update_notification_preferences(
        user_id=current_user.id,
        preferences=preferences
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Get all users (admin only)."""
    return container.user_service.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Get user by ID (admin only)."""
    user = container.user_service.get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Update user (admin only)."""
    updated_user = container.user_service.update_user(
        user_id=user_id,
        user=user_update
    )
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Delete user (admin only)."""
    if not container.user_service.delete_user(user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) 