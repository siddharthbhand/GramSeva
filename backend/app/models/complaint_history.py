from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    DateTime,
    Enum,
)

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.core.enums import ComplaintStatus


class ComplaintHistory(Base):
    __tablename__ = "complaint_history"

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

    old_status = Column(
        Enum(ComplaintStatus),
        nullable=False,
    )

    new_status = Column(
        Enum(ComplaintStatus),
        nullable=False,
    )

    changed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    remarks = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ==========================================
    # Relationships
    # ==========================================

    complaint = relationship(
        "Complaint",
        back_populates="history",
    )

    changed_by_user = relationship(
        "User",
        back_populates="complaint_history",
    )