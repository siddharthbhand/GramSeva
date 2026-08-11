from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class ComplaintEscalation(Base):
    __tablename__ = "complaint_escalations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    complaint_id = Column(
        Integer,
        ForeignKey("complaints.id"),
        nullable=False,
    )

    escalation_level = Column(
        Integer,
        nullable=False,
        default=1,
    )

    escalated_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    escalated_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    reason = Column(
        Text,
        nullable=False,
    )

    remarks = Column(
        Text,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    escalated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # =====================================================
    # Relationships
    # =====================================================

    complaint = relationship(
        "Complaint",
        back_populates="escalations",
    )

    escalated_to_user = relationship(
        "User",
        foreign_keys=[escalated_to],
    )

    escalated_by_user = relationship(
        "User",
        foreign_keys=[escalated_by],
    )