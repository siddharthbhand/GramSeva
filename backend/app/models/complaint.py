from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base
from app.core.enums import ComplaintStatus


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    location = Column(
        String(255),
        nullable=False,
    )

    status = Column(
        Enum(ComplaintStatus),
        nullable=False,
        default=ComplaintStatus.PENDING,
    )

    priority = Column(
        String(50),
        nullable=False,
        default="Medium",
    )

    citizen_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # =====================================================
    # Relationships
    # =====================================================

    citizen = relationship(
        "User",
        back_populates="complaints",
        foreign_keys=[citizen_id],
    )

    department = relationship(
        "Department",
        back_populates="complaints",
    )

    assignments = relationship(
        "ComplaintAssignment",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    history = relationship(
        "ComplaintHistory",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )