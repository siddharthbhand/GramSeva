from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    # =====================================================
    # Basic User Information
    # =====================================================

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
    # Department
    # =====================================================

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    # User's department
    department = relationship(
        "Department",
        back_populates="users",
    )

    # Complaints created by this user as citizen
    complaints = relationship(
        "Complaint",
        back_populates="citizen",
        foreign_keys="Complaint.citizen_id",
    )

    # Complaints assigned to this user as officer
    assigned_complaints = relationship(
        "ComplaintAssignment",
        foreign_keys="ComplaintAssignment.officer_id",
        back_populates="officer",
    )

    # Assignments created by this user
    created_assignments = relationship(
        "ComplaintAssignment",
        foreign_keys="ComplaintAssignment.assigned_by",
        back_populates="assigned_by_user",
    )

    # Complaint history changes made by this user
    complaint_history = relationship(
        "ComplaintHistory",
        back_populates="changed_by_user",
    )

    # =====================================================
    # Complaint Escalation Relationships
    # =====================================================

    # Escalations received by this user
    escalations_received = relationship(
        "ComplaintEscalation",
        foreign_keys="ComplaintEscalation.escalated_to",
        back_populates="escalated_to_user",
    )

    # Escalations created by this user
    escalations_created = relationship(
        "ComplaintEscalation",
        foreign_keys="ComplaintEscalation.escalated_by",
        back_populates="escalated_by_user",
    )