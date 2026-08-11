from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.sql import func

from app.db.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    # =====================================================
    # Primary Key
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # Notification Recipient
    # =====================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    # =====================================================
    # Related Complaint
    # =====================================================

    complaint_id = Column(
        Integer,
        ForeignKey("complaints.id"),
        nullable=True,
    )

    # =====================================================
    # Related Escalation
    # =====================================================

    escalation_id = Column(
        Integer,
        ForeignKey("complaint_escalations.id"),
        nullable=True,
    )

    # =====================================================
    # Notification Content
    # =====================================================

    title = Column(
        String(255),
        nullable=False,
    )

    message = Column(
        Text,
        nullable=False,
    )

    # =====================================================
    # Notification Type
    # =====================================================

    notification_type = Column(
        String(50),
        nullable=False,
    )

    # =====================================================
    # Read Status
    # =====================================================

    is_read = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    read_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =====================================================
    # Active Status
    # =====================================================

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    # =====================================================
    # Timestamp
    # =====================================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )