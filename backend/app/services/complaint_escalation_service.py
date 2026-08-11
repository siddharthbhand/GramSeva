from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_escalation import ComplaintEscalation
from app.models.complaint_assignment import ComplaintAssignment
from app.models.user import User

from app.schemas.complaint_escalation import (
    ComplaintEscalationCreate,
    ComplaintEscalationUpdate,
)


class ComplaintEscalationService:

    # =====================================================
    # Create Complaint Escalation
    # =====================================================

    @staticmethod
    def create_escalation(
        db: Session,
        escalation_data: ComplaintEscalationCreate,
        escalated_by: int,
    ):

        # -------------------------------------------------
        # Check Complaint
        # -------------------------------------------------

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == escalation_data.complaint_id,
                Complaint.is_active == True,
            )
            .first()
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found.",
            )

        # -------------------------------------------------
        # Check Escalated User
        # -------------------------------------------------

        if escalation_data.escalated_to is not None:

            escalated_user = (
                db.query(User)
                .filter(
                    User.id == escalation_data.escalated_to,
                    User.is_active == True,
                )
                .first()
            )

            if not escalated_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Escalation target user not found.",
                )

        # -------------------------------------------------
        # Check Escalating User
        # -------------------------------------------------

        escalating_user = (
            db.query(User)
            .filter(
                User.id == escalated_by,
                User.is_active == True,
            )
            .first()
        )

        if not escalating_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Escalating user not found.",
            )

        # -------------------------------------------------
        # Calculate Next Escalation Level
        # -------------------------------------------------

        latest_escalation = (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.complaint_id
                == escalation_data.complaint_id,
            )
            .order_by(
                ComplaintEscalation.escalation_level.desc()
            )
            .first()
        )

        if latest_escalation:
            escalation_level = (
                latest_escalation.escalation_level + 1
            )
        else:
            escalation_level = 1

        # -------------------------------------------------
        # Create Escalation
        # -------------------------------------------------

        escalation = ComplaintEscalation(
            complaint_id=escalation_data.complaint_id,
            escalation_level=escalation_level,
            escalated_to=escalation_data.escalated_to,
            escalated_by=escalated_by,
            reason=escalation_data.reason,
            remarks=escalation_data.remarks,
            is_active=True,
        )

        db.add(escalation)
        db.commit()
        db.refresh(escalation)

        return escalation

    # =====================================================
    # Automatic SLA Escalation
    # =====================================================

    @staticmethod
    def auto_escalate_complaint(
        db: Session,
        complaint_id: int,
    ):

        # -------------------------------------------------
        # Check Complaint
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Check SLA Due Date
        # -------------------------------------------------

        if complaint.sla_due_at is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SLA due date is not configured for this complaint.",
            )

        current_time = datetime.utcnow()

        if current_time < complaint.sla_due_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complaint SLA has not been breached yet.",
            )

        # -------------------------------------------------
        # Check Existing Automatic Escalation
        # -------------------------------------------------

        existing_escalation = (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.complaint_id == complaint_id,
                ComplaintEscalation.is_active == True,
                ComplaintEscalation.reason
                == "Automatic escalation due to SLA breach.",
            )
            .first()
        )

        if existing_escalation:
            return existing_escalation

        # -------------------------------------------------
        # Find Active Complaint Assignment
        # -------------------------------------------------

        assignment = (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.complaint_id == complaint_id,
                ComplaintAssignment.is_active == True,
            )
            .order_by(
                ComplaintAssignment.assigned_at.desc()
            )
            .first()
        )

        # -------------------------------------------------
        # Determine Escalation Target
        # -------------------------------------------------

        escalated_to = None

        if assignment:

            officer = (
                db.query(User)
                .filter(
                    User.id == assignment.officer_id,
                    User.is_active == True,
                )
                .first()
            )

            if officer:
                escalated_to = officer.id

        # -------------------------------------------------
        # Calculate Next Escalation Level
        # -------------------------------------------------

        latest_escalation = (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.complaint_id == complaint_id,
            )
            .order_by(
                ComplaintEscalation.escalation_level.desc()
            )
            .first()
        )

        if latest_escalation:
            escalation_level = (
                latest_escalation.escalation_level + 1
            )
        else:
            escalation_level = 1

        # -------------------------------------------------
        # Create Automatic Escalation
        # -------------------------------------------------

        escalation = ComplaintEscalation(
            complaint_id=complaint_id,
            escalation_level=escalation_level,
            escalated_to=escalated_to,
            escalated_by=None,
            reason="Automatic escalation due to SLA breach.",
            remarks=(
                "Complaint SLA deadline has been exceeded. "
                "System automatically escalated the complaint "
                "to the currently assigned responsible officer."
            ),
            is_active=True,
        )

        # -------------------------------------------------
        # Mark SLA As Breached
        # -------------------------------------------------

        complaint.is_sla_breached = True

        db.add(escalation)
        db.commit()
        db.refresh(escalation)

        return escalation

    # =====================================================
    # Get Escalation By ID
    # =====================================================

    @staticmethod
    def get_escalation_by_id(
        db: Session,
        escalation_id: int,
    ):

        escalation = (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.id == escalation_id,
                ComplaintEscalation.is_active == True,
            )
            .first()
        )

        if not escalation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Escalation not found.",
            )

        return escalation

    # =====================================================
    # Get Escalations By Complaint
    # =====================================================

    @staticmethod
    def get_escalations_by_complaint(
        db: Session,
        complaint_id: int,
    ):

        # -------------------------------------------------
        # Check Complaint
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Get Escalation History
        # -------------------------------------------------

        return (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.complaint_id == complaint_id,
                ComplaintEscalation.is_active == True,
            )
            .order_by(
                ComplaintEscalation.escalation_level.asc()
            )
            .all()
        )

    # =====================================================
    # Get All Escalations
    # =====================================================

    @staticmethod
    def get_all_escalations(
        db: Session,
    ):

        return (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.is_active == True,
            )
            .order_by(
                ComplaintEscalation.id.desc()
            )
            .all()
        )

    # =====================================================
    # Update Escalation
    # =====================================================

    @staticmethod
    def update_escalation(
        db: Session,
        escalation_id: int,
        escalation_data: ComplaintEscalationUpdate,
    ):

        escalation = (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.id == escalation_id,
                ComplaintEscalation.is_active == True,
            )
            .first()
        )

        if not escalation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Escalation not found.",
            )

        # -------------------------------------------------
        # Validate Escalation Target
        # -------------------------------------------------

        if escalation_data.escalated_to is not None:

            escalated_user = (
                db.query(User)
                .filter(
                    User.id == escalation_data.escalated_to,
                    User.is_active == True,
                )
                .first()
            )

            if not escalated_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Escalation target user not found.",
                )

        # -------------------------------------------------
        # Update Escalation
        # -------------------------------------------------

        escalation.escalation_level = (
            escalation_data.escalation_level
        )

        escalation.escalated_to = (
            escalation_data.escalated_to
        )

        escalation.reason = escalation_data.reason

        escalation.remarks = escalation_data.remarks

        escalation.is_active = (
            escalation_data.is_active
        )

        db.commit()
        db.refresh(escalation)

        return escalation

    # =====================================================
    # Delete Escalation (Soft Delete)
    # =====================================================

    @staticmethod
    def delete_escalation(
        db: Session,
        escalation_id: int,
    ):

        escalation = (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.id == escalation_id,
            )
            .first()
        )

        if not escalation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Escalation not found.",
            )

        if escalation.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Escalation is already deactivated.",
            )

        escalation.is_active = False

        db.commit()

        return {
            "message": "Escalation deactivated successfully."
        }