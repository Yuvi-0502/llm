from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.notification import NotificationResponse, UserPreferenceResponse, UserPreferenceUpdate
from controllers.notification_controller import NotificationController
from Utils.jwt_handler import get_current_user
from typing import List

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    unread_only: bool = Query(False, description="Show only unread notifications"),
    current_user=Depends(get_current_user)
):
    """Get notifications for the current user"""
    try:
        controller = NotificationController()
        return controller.get_user_notifications(current_user["user_id"], unread_only)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user=Depends(get_current_user)
):
    """Mark a notification as read"""
    try:
        controller = NotificationController()
        return controller.mark_notification_as_read(notification_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/preferences", response_model=UserPreferenceResponse)
def get_preferences(current_user=Depends(get_current_user)):
    """Get current user's notification preferences"""
    try:
        controller = NotificationController()
        return controller.get_user_preferences(current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/preferences", response_model=UserPreferenceResponse)
def update_preferences(
    preferences: UserPreferenceUpdate,
    current_user=Depends(get_current_user)
):
    """Update current user's notification preferences"""
    try:
        controller = NotificationController()
        return controller.update_user_preferences(
            current_user["user_id"],
            preferences.category_id,
            preferences.keywords,
            preferences.email_notifications
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 