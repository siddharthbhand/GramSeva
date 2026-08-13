from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.enums import ComplaintStatus
from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationCreate
from app.services.notification_service import NotificationService
from app.utils.sla import SLAUtils


class SLAAutomationService:

    # =====================================================
    # Active SLA Statuses
    # =====================================================

    ACTIVE_STATUSES = {
        ComplaintStatus.PENDING,
        ComplaintStatus.ASSIGNED,
        ComplaintStatus.IN_PROGRESS,
        ComplaintStatus.REOPENED,
    }

    # =====================================================
    # Get Active SLA Complaints
    # =====================================================

    @staticmethod
    def get_active_sla_complaints(
        db: Session,
    ):
        """
        Return active complaints whose status requires
        ongoing SLA monitoring.
        """

        return (
            db.query(Complaint)
            .filter(
                Complaint.is_active == True,
                Complaint.status.in_(
                    list(
                        SLAAutomationService.ACTIVE_STATUSES
                    )
                ),
                Complaint.sla_due_at.isnot(None),
            )
            .order_by(
                Complaint.sla_due_at.asc()
            )
            .all()
        )

    # =====================================================
    # Evaluate Complaint SLA
    # =====================================================

    @staticmethod
    def evaluate_complaint_sla(
        complaint: Complaint,
    ) -> str:
        """
        Evaluate the current SLA state of a complaint.
        """

        if complaint.sla_due_at is None:
            return "Unknown"

        if SLAUtils.is_breached(
            complaint.sla_due_at
        ):
            return "Breached"

        if SLAUtils.is_near_breach(
            complaint.sla_due_at
        ):
            return "Near Breach"

        return "Within SLA"

    # =====================================================
    # Get Near Breach Complaints
    # =====================================================

    @staticmethod
    def get_near_breach_complaints(
        db: Session,
    ):
        """
        Return active complaints that are close to
        reaching their SLA deadline.
        """

        complaints = (
            SLAAutomationService.get_active_sla_complaints(
                db
            )
        )

        return [
            complaint
            for complaint in complaints
            if SLAAutomationService.evaluate_complaint_sla(
                complaint
            )
            == "Near Breach"
        ]

    # =====================================================
    # Get Breached Complaints
    # =====================================================

    @staticmethod
    def get_breached_complaints(
        db: Session,
    ):
        """
        Return active complaints whose SLA has expired.
        """

        complaints = (
            SLAAutomationService.get_active_sla_complaints(
                db
            )
        )

        return [
            complaint
            for complaint in complaints
            if SLAAutomationService.evaluate_complaint_sla(
                complaint
            )
            == "Breached"
        ]

    # =====================================================
    # Check Existing SLA Warning
    # =====================================================

    @staticmethod
    def has_sla_warning_notification(
        db: Session,
        complaint_id: int,
        user_id: int,
    ) -> bool:
        """
        Prevent duplicate SLA warning notifications
        for the same complaint and user.
        """

        notification = (
            db.query(Notification)
            .filter(
                Notification.complaint_id == complaint_id,
                Notification.user_id == user_id,
                Notification.notification_type
                == "SLA_WARNING",
                Notification.is_active == True,
            )
            .first()
        )

        return notification is not None

    # =====================================================
    # Get Active Complaint Officer
    # =====================================================

    @staticmethod
    def get_active_assignment_officer(
        db: Session,
        complaint_id: int,
    ):
        """
        Return the officer currently assigned to the
        complaint.
        """

        assignment = (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.complaint_id
                == complaint_id,
                ComplaintAssignment.is_active == True,
            )
            .order_by(
                ComplaintAssignment.assigned_at.desc()
            )
            .first()
        )

        if not assignment:
            return None

        officer = (
            db.query(User)
            .filter(
                User.id == assignment.officer_id,
                User.is_active == True,
            )
            .first()
        )

        return officer

    # =====================================================
    # Create SLA Warning Notification
    # =====================================================

    @staticmethod
    def create_sla_warning_notification(
        db: Session,
        complaint: Complaint,
    ):
        """
        Create a warning notification for the officer
        responsible for the complaint.

        Duplicate warnings are prevented.
        """

        officer = (
            SLAAutomationService.get_active_assignment_officer(
                db=db,
                complaint_id=complaint.id,
            )
        )

        if not officer:
            return None

        if SLAAutomationService.has_sla_warning_notification(
            db=db,
            complaint_id=complaint.id,
            user_id=officer.id,
        ):
            return None

        remaining_hours = SLAUtils.get_remaining_hours(
            complaint.sla_due_at
        )

        remaining_hours = max(
            0,
            round(remaining_hours, 2),
        )

        notification_data = NotificationCreate(
            user_id=officer.id,
            complaint_id=complaint.id,
            escalation_id=None,
            title="SLA Warning",
            message=(
                f"Complaint #{complaint.id} is approaching "
                f"its SLA deadline. Approximately "
                f"{remaining_hours} hour(s) remaining. "
                "Please take action before the SLA expires."
            ),
            notification_type="SLA_WARNING",
        )

        return NotificationService.create_notification(
            db=db,
            notification_data=notification_data,
        )

    # =====================================================
    # Process Near Breach Complaint
    # =====================================================

    @staticmethod
    def process_near_breach_complaint(
        db: Session,
        complaint: Complaint,
    ):
        """
        Process a single near-breach complaint.
        """

        sla_status = (
            SLAAutomationService.evaluate_complaint_sla(
                complaint
            )
        )

        if sla_status != "Near Breach":
            return None

        return (
            SLAAutomationService
            .create_sla_warning_notification(
                db=db,
                complaint=complaint,
            )
        )

    # =====================================================
    # Process All Near Breach Complaints
    # =====================================================

    @staticmethod
    def process_near_breach_complaints(
        db: Session,
    ):
        """
        Process all currently near-breach complaints.
        """

        complaints = (
            SLAAutomationService.get_near_breach_complaints(
                db
            )
        )

        notifications_created = []

        for complaint in complaints:

            notification = (
                SLAAutomationService
                .process_near_breach_complaint(
                    db=db,
                    complaint=complaint,
                )
            )

            if notification:
                notifications_created.append(
                    notification
                )

        return notifications_created

    # =====================================================
    # Get SLA Monitoring Summary
    # =====================================================

    @staticmethod
    def get_monitoring_summary(
        db: Session,
    ):
        """
        Return a summary of complaints currently being
        monitored by the SLA automation layer.
        """

        complaints = (
            SLAAutomationService.get_active_sla_complaints(
                db
            )
        )

        within_sla = 0
        near_breach = 0
        breached = 0

        for complaint in complaints:

            sla_status = (
                SLAAutomationService.evaluate_complaint_sla(
                    complaint
                )
            )

            if sla_status == "Within SLA":
                within_sla += 1

            elif sla_status == "Near Breach":
                near_breach += 1

            elif sla_status == "Breached":
                breached += 1

        return {
            "total_monitored": len(complaints),
            "within_sla": within_sla,
            "near_breach": near_breach,
            "breached": breached,
            "checked_at": datetime.now(
                timezone.utc
            ),
        }