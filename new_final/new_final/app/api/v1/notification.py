from fastapi import APIRouter, HTTPException
from app.schemas.notification import NotificationCreate, NotificationOut
from app.services.notification_service import NotificationService
from typing import List

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=NotificationOut)
def create_notification(notification: NotificationCreate):
    service = NotificationService()
    return service.create_notification(notification)

@router.get("/user/{user_id}", response_model=List[NotificationOut])
def get_notifications_for_user(user_id: int):
    service = NotificationService()
    return service.get_notifications_for_user(user_id)

@router.put("/{notification_id}/read", response_model=NotificationOut)
def mark_notification_as_read(notification_id: int):
    service = NotificationService()
    notification = service.mark_notification_as_read(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification 