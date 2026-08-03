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

    complaint = relationship(
        "Complaint",
        foreign_keys=[complaint_id],
    )

    officer = relationship(
        "User",
        foreign_keys=[officer_id],
    )

    assigned_by_user = relationship(
        "User",
        foreign_keys=[assigned_by],
    )