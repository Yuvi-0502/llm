from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import User, UserKeyword
from app.schemas.notification import NotificationResponse, NotificationPreferences
from app.services.email_service import send_article_notification, send_keyword_notification

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user's notifications.
    """
    # In a real application, you would have a Notifications table
    # For this example, we'll return an empty list
    return []


@router.put("/preferences", response_model=NotificationPreferences)
def update_notification_preferences(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    preferences: NotificationPreferences,
) -> Any:
    """
    Update user's notification preferences.
    """
    # Update category preferences
    current_user.notification_preferences = []
    for category_name, enabled in preferences.categories.items():
        if enabled:
            category = db.query(Category).filter(Category.name == category_name).first()
            if category:
                current_user.notification_preferences.append(category)
    
    db.commit()
    return preferences


@router.post("/keywords", response_model=Dict[str, str])
def add_keyword(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    keyword: str,
) -> Any:
    """
    Add a keyword for notifications.
    """
    # Check if keyword already exists
    existing_keyword = db.query(UserKeyword).filter(
        UserKeyword.user_id == current_user.id,
        UserKeyword.keyword == keyword
    ).first()
    
    if existing_keyword:
        raise HTTPException(status_code=400, detail="Keyword already exists")
    
    # Create new keyword
    user_keyword = UserKeyword(user_id=current_user.id, keyword=keyword)
    db.add(user_keyword)
    db.commit()
    
    return {"message": "Keyword added successfully"}


@router.delete("/keywords/{keyword}", response_model=Dict[str, str])
def remove_keyword(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    keyword: str,
) -> Any:
    """
    Remove a keyword.
    """
    user_keyword = db.query(UserKeyword).filter(
        UserKeyword.user_id == current_user.id,
        UserKeyword.keyword == keyword
    ).first()
    
    if not user_keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    db.delete(user_keyword)
    db.commit()
    
    return {"message": "Keyword removed successfully"} 