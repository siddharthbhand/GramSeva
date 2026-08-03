from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import ComplaintStatus
from app.core.status_transition import is_valid_transition

from app.models.complaint import Complaint
from app.models.department import Department

from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintStatusUpdate,
)

from app.services.complaint_history_service import ComplaintHistoryService


class ComplaintService:

    # =====================================================
    # Create Complaint
    # =====================================================

    @staticmethod
    def create_complaint(
        db: Session,
        complaint_data: ComplaintCreate,
        citizen_id: int,
    ):

        department = None

        if complaint_data.department_id is not None:

            department = (
                db.query(Department)
                .filter(
                    Department.id == complaint_data.department_id,
                    Department.is_active == True,
                )
                .first()
            )

            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Department not found.",
                )

        # =====================================================
        # SLA Calculation
        # =====================================================

        sla_hours = 24
        sla_due_at = datetime.utcnow() + timedelta(hours=sla_hours)

        complaint = Complaint(
            title=complaint_data.title,
            description=complaint_data.description,
            location=complaint_data.location,
            status=ComplaintStatus.PENDING,
            priority=complaint_data.priority,
            citizen_id=citizen_id,
            department_id=complaint_data.department_id,

            # SLA Fields
            sla_hours=sla_hours,
            sla_due_at=sla_due_at,
            is_sla_breached=False,
        )

        db.add(complaint)
        db.commit()
        db.refresh(complaint)

        return complaint

    # =====================================================
    # Get All Complaints
    # =====================================================

    @staticmethod
    def get_all_complaints(db: Session):

        return (
            db.query(Complaint)
            .filter(
                Complaint.is_active == True,
            )
            .order_by(Complaint.id)
            .all()
        )

    # =====================================================
    # Get Complaint By ID
    # =====================================================

    @staticmethod
    def get_complaint_by_id(
        db: Session,
        complaint_id: int,
    ):

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == complaint_id,
                Complaint.is_active == True,
            )
            .first()
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found.",
            )

        return complaint

    # =====================================================
    # Update Complaint
    # =====================================================

    @staticmethod
    def update_complaint(
        db: Session,
        complaint_id: int,
        complaint_data: ComplaintUpdate,
    ):

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == complaint_id,
                Complaint.is_active == True,
            )
            .first()
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found.",
            )

        if complaint_data.department_id is not None:

            department = (
                db.query(Department)
                .filter(
                    Department.id == complaint_data.department_id,
                    Department.is_active == True,
                )
                .first()
            )

            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Department not found.",
                )

        complaint.title = complaint_data.title
        complaint.description = complaint_data.description
        complaint.location = complaint_data.location
        complaint.status = complaint_data.status
        complaint.priority = complaint_data.priority
        complaint.department_id = complaint_data.department_id
        complaint.is_active = complaint_data.is_active

        db.commit()
        db.refresh(complaint)

        return complaint

    # =====================================================
    # Update Complaint Status
    # =====================================================

    @staticmethod
    def update_complaint_status(
        db: Session,
        complaint_id: int,
        status_data: ComplaintStatusUpdate,
        changed_by: int,
    ):

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == complaint_id,
                Complaint.is_active == True,
            )
            .first()
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found.",
            )

        current_status = ComplaintStatus(complaint.status)
        old_status = current_status
        new_status = status_data.status

        if not is_valid_transition(
            current_status,
            new_status,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid status transition "
                    f"from {current_status.value} "
                    f"to {new_status.value}."
                ),
            )

        complaint.status = new_status

        db.commit()
        db.refresh(complaint)

        ComplaintHistoryService.create_history(
            db=db,
            complaint_id=complaint.id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            remarks=f"Status changed from {old_status.value} to {new_status.value}",
        )

        return complaint

    # =====================================================
    # Delete Complaint (Soft Delete)
    # =====================================================

    @staticmethod
    def delete_complaint(
        db: Session,
        complaint_id: int,
    ):

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == complaint_id,
            )
            .first()
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found.",
            )

        if complaint.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complaint is already deactivated.",
            )

        complaint.is_active = False

        db.commit()

        return {
            "message": "Complaint deactivated successfully."
        }