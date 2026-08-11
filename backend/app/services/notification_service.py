from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User
from app.models.complaint import Complaint
from app.models.complaint_escalation import ComplaintEscalation

from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)


class NotificationService:

    # =====================================================
    # Create Notification
    # =====================================================

    @staticmethod
    def create_notification(
        db: Session,
        notification_data: NotificationCreate,
    ):

        # -------------------------------------------------
        # Check User
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(
                User.id == notification_data.user_id,
                User.is_active == True,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification recipient user not found.",
            )

        # -------------------------------------------------
        # Check Complaint
        # -------------------------------------------------

        if notification_data.complaint_id is not None:

            complaint = (
                db.query(Complaint)
                .filter(
                    Complaint.id
                    == notification_data.complaint_id,
                    Complaint.is_active == True,
                )
                .first()
            )

            if not complaint:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Related complaint not found.",
                )

        # -------------------------------------------------
        # Check Escalation
        # -------------------------------------------------

        if notification_data.escalation_id is not None:

            escalation = (
                db.query(ComplaintEscalation)
                .filter(
                    ComplaintEscalation.id
                    == notification_data.escalation_id,
                    ComplaintEscalation.is_active == True,
                )
                .first()
            )

            if not escalation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Related escalation not found.",
                )

        # -------------------------------------------------
        # Create Notification
        # -------------------------------------------------

        notification = Notification(
            user_id=notification_data.user_id,
            complaint_id=notification_data.complaint_id,
            escalation_id=notification_data.escalation_id,
            title=notification_data.title,
            message=notification_data.message,
            notification_type=notification_data.notification_type,
            is_read=False,
            is_active=True,
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    # =====================================================
    # Get Notification By ID
    # =====================================================

    @staticmethod
    def get_notification_by_id(
        db: Session,
        notification_id: int,
    ):

        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.is_active == True,
            )
            .first()
        )

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found.",
            )

        return notification

    # =====================================================
    # Get All Notifications
    # =====================================================

    @staticmethod
    def get_all_notifications(
        db: Session,
    ):

        return (
            db.query(Notification)
            .filter(
                Notification.is_active == True,
            )
            .order_by(
                Notification.id.desc()
            )
            .all()
        )

    # =====================================================
    # Get Notifications By User
    # =====================================================

    @staticmethod
    def get_notifications_by_user(
        db: Session,
        user_id: int,
    ):

        # -------------------------------------------------
        # Check User
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(
                User.id == user_id,
                User.is_active == True,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        # -------------------------------------------------
        # Get User Notifications
        # -------------------------------------------------

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_active == True,
            )
            .order_by(
                Notification.id.desc()
            )
            .all()
        )

    # =====================================================
    # Get Unread Notifications By User
    # =====================================================

    @staticmethod
    def get_unread_notifications(
        db: Session,
        user_id: int,
    ):

        # -------------------------------------------------
        # Check User
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(
                User.id == user_id,
                User.is_active == True,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        # -------------------------------------------------
        # Get Unread Notifications
        # -------------------------------------------------

        return (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.is_active == True,
            )
            .order_by(
                Notification.id.desc()
            )
            .all()
        )

    # =====================================================
    # Mark Notification As Read
    # =====================================================

    @staticmethod
    def mark_as_read(
        db: Session,
        notification_id: int,
    ):

        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.is_active == True,
            )
            .first()
        )

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found.",
            )

        # -------------------------------------------------
        # Already Read
        # -------------------------------------------------

        if notification.is_read:
            return notification

        # -------------------------------------------------
        # Mark As Read
        # -------------------------------------------------

        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(notification)

        return notification

    # =====================================================
    # Mark All User Notifications As Read
    # =====================================================

    @staticmethod
    def mark_all_as_read(
        db: Session,
        user_id: int,
    ):

        # -------------------------------------------------
        # Check User
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(
                User.id == user_id,
                User.is_active == True,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        # -------------------------------------------------
        # Get Unread Notifications
        # -------------------------------------------------

        notifications = (
            db.query(Notification)
            .filter(
                Notification.user_id == user_id,
                Notification.is_read == False,
                Notification.is_active == True,
            )
            .all()
        )

        current_time = datetime.now(timezone.utc)

        for notification in notifications:
            notification.is_read = True
            notification.read_at = current_time

        db.commit()

        return {
            "message": "All notifications marked as read.",
            "updated_count": len(notifications),
        }

    # =====================================================
    # Update Notification
    # =====================================================

    @staticmethod
    def update_notification(
        db: Session,
        notification_id: int,
        notification_data: NotificationUpdate,
    ):

        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
                Notification.is_active == True,
            )
            .first()
        )

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found.",
            )

        # -------------------------------------------------
        # Update Fields
        # -------------------------------------------------

        if notification_data.title is not None:
            notification.title = notification_data.title

        if notification_data.message is not None:
            notification.message = notification_data.message

        if notification_data.notification_type is not None:
            notification.notification_type = (
                notification_data.notification_type
            )

        if notification_data.is_read is not None:

            notification.is_read = (
                notification_data.is_read
            )

            if notification_data.is_read:
                notification.read_at = datetime.now(
                    timezone.utc
                )
            else:
                notification.read_at = None

        if notification_data.is_active is not None:
            notification.is_active = (
                notification_data.is_active
            )

        db.commit()
        db.refresh(notification)

        return notification

    # =====================================================
    # Delete Notification (Soft Delete)
    # =====================================================

    @staticmethod
    def delete_notification(
        db: Session,
        notification_id: int,
    ):

        notification = (
            db.query(Notification)
            .filter(
                Notification.id == notification_id,
            )
            .first()
        )

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found.",
            )

        if notification.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification is already deactivated.",
            )

        notification.is_active = False

        db.commit()

        return {
            "message": "Notification deactivated successfully."
        }