from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_history import ComplaintHistory
from app.core.enums import ComplaintStatus


class ComplaintHistoryService:

    # =====================================================
    # Create Complaint History
    # =====================================================

    @staticmethod
    def create_history(
        db: Session,
        complaint_id: int,
        old_status: ComplaintStatus,
        new_status: ComplaintStatus,
        changed_by: int,
        remarks: str | None = None,
    ):

        history = ComplaintHistory(
            complaint_id=complaint_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            remarks=remarks,
        )

        db.add(history)
        db.commit()
        db.refresh(history)

        return history

    # =====================================================
    # Get Complaint History
    # =====================================================

    @staticmethod
    def get_complaint_history(
        db: Session,
        complaint_id: int,
        citizen_id: int,
    ):

        # -------------------------------------------------
        # Verify complaint belongs to logged-in citizen
        # -------------------------------------------------

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == complaint_id,
                Complaint.citizen_id == citizen_id,
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
        # Get history
        # -------------------------------------------------

        return (
            db.query(ComplaintHistory)
            .filter(
                ComplaintHistory.complaint_id == complaint_id,
            )
            .order_by(
                ComplaintHistory.created_at.asc()
            )
            .all()
        )

    # =====================================================
    # Get History By ID
    # =====================================================

    @staticmethod
    def get_history_by_id(
        db: Session,
        history_id: int,
        citizen_id: int,
    ):

        history = (
            db.query(ComplaintHistory)
            .join(
                Complaint,
                Complaint.id == ComplaintHistory.complaint_id,
            )
            .filter(
                ComplaintHistory.id == history_id,
                Complaint.citizen_id == citizen_id,
                Complaint.is_active == True,
            )
            .first()
        )

        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint history not found.",
            )

        return history