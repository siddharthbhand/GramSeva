from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)

from app.services.notification_service import (
    NotificationService,
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# =====================================================
# Create Notification
# =====================================================

@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.create_notification(
        db=db,
        notification_data=notification_data,
    )


# =====================================================
# Get All Notifications
# =====================================================

@router.get(
    "/",
    response_model=List[NotificationResponse],
)
def get_all_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.get_all_notifications(
        db=db,
    )


# =====================================================
# Get Notifications By User
# =====================================================

@router.get(
    "/user/{user_id}",
    response_model=List[NotificationResponse],
)
def get_notifications_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.get_notifications_by_user(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Get Unread Notifications
# =====================================================

@router.get(
    "/user/{user_id}/unread",
    response_model=List[NotificationResponse],
)
def get_unread_notifications(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.get_unread_notifications(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Get Notification By ID
# =====================================================

@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def get_notification_by_id(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.get_notification_by_id(
        db=db,
        notification_id=notification_id,
    )


# =====================================================
# Mark Notification As Read
# =====================================================

@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.mark_as_read(
        db=db,
        notification_id=notification_id,
    )


# =====================================================
# Mark All Notifications As Read
# =====================================================

@router.put(
    "/user/{user_id}/read-all",
)
def mark_all_notifications_as_read(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.mark_all_as_read(
        db=db,
        user_id=user_id,
    )


# =====================================================
# Update Notification
# =====================================================

@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
)
def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.update_notification(
        db=db,
        notification_id=notification_id,
        notification_data=notification_data,
    )


# =====================================================
# Delete Notification
# =====================================================

@router.delete(
    "/{notification_id}",
)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return NotificationService.delete_notification(
        db=db,
        notification_id=notification_id,
    )