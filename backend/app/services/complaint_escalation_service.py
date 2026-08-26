from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_escalation import ComplaintEscalation
from app.models.complaint_assignment import ComplaintAssignment
from app.models.notification import Notification
from app.models.user import User

from app.schemas.complaint_escalation import (
    ComplaintEscalationCreate,
    ComplaintEscalationUpdate,
)
from app.services.escalation_hierarchy_service import (
    EscalationHierarchyService,
)
from app.services.sla_automation_service import (
    SLAAutomationService,
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

        # -------------------------------------------------
        # Generate Escalation ID
        # -------------------------------------------------

        db.flush()

        # -------------------------------------------------
        # Create Escalation Notification
        # -------------------------------------------------

        if escalation_data.escalated_to is not None:

            notification = Notification(
                user_id=escalation_data.escalated_to,
                complaint_id=complaint.id,
                escalation_id=escalation.id,
                title="Complaint Escalated",
                message=(
                    f"Complaint #{complaint.id} has been "
                    "escalated to you for further action."
                ),
                notification_type="COMPLAINT_ESCALATED",
                is_read=False,
                is_active=True,
            )

            db.add(notification)

        # -------------------------------------------------
        # Commit Escalation + Notification Together
        # -------------------------------------------------

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
        """
        Trigger the centralized SLA automation engine for
        a single complaint.

        The SLA automation service is the single source of
        truth for automatic escalation hierarchy, target
        selection, and escalation notifications.
        """

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

        result = (
            SLAAutomationService
            .process_breached_complaint(
                db=db,
                complaint=complaint,
            )
        )

        if result is None:

            latest_escalation = (
                SLAAutomationService
                .get_latest_escalation(
                    db=db,
                    complaint_id=complaint_id,
                )
            )

            if latest_escalation is not None:

                next_level = (
                    EscalationHierarchyService
                    .get_next_escalation_level(
                        db=db,
                        complaint_id=complaint_id,
                    )
                )

                if next_level is None:

                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=(
                            "No further escalation is available "
                            "for this complaint. The maximum "
                            "configured escalation level has "
                            "already been reached."
                        ),
                    )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Automatic escalation could not be created. "
                    "Verify that the complaint SLA is breached "
                    "and an eligible escalation target is available."
                ),
            )

        return result["escalation"]

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