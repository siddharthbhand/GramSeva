from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    full_name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    phone = Column(
        String(15),
        unique=True,
        nullable=False,
    )

    password = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(30),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    complaints = relationship(
        "Complaint",
        back_populates="citizen",
        foreign_keys="Complaint.citizen_id",
    )

    assigned_complaints = relationship(
        "ComplaintAssignment",
        foreign_keys="ComplaintAssignment.officer_id",
        back_populates="officer",
    )

    created_assignments = relationship(
        "ComplaintAssignment",
        foreign_keys="ComplaintAssignment.assigned_by",
        back_populates="assigned_by_user",
    )

    complaint_history = relationship(
        "ComplaintHistory",
        back_populates="changed_by_user",
    )