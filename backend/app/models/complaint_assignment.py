from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class ComplaintAssignment(Base):
    __tablename__ = "complaint_assignments"

    id = Column(Integer, primary_key=True, index=True)

    complaint_id = Column(
        Integer,
        ForeignKey("complaints.id"),
        nullable=False,
    )

    officer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    assigned_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    remarks = Column(
        Text,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    assigned_at = Column(
        DateTime,
        server_default=func.now(),
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ============================
    # Relationships
    # ============================

    complaint = relationship(
        "Complaint",
        back_populates="assignments",
    )

    officer = relationship(
        "User",
        foreign_keys=[officer_id],
        back_populates="assigned_complaints",
    )

    assigned_by_user = relationship(
        "User",
        foreign_keys=[assigned_by],
        back_populates="created_assignments",
    )