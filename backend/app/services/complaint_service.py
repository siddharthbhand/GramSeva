from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import ComplaintStatus
from app.core.status_transition import is_valid_transition
from app.core.user_roles import UserRole

from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.models.complaint_history import ComplaintHistory
from app.models.department import Department
from app.models.notification import Notification
from app.models.user import User

from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintStatusUpdate,
    ComplaintSLAResponse,
)

from app.services.complaint_history_service import ComplaintHistoryService
from app.utils.sla import SLAUtils


class ComplaintService:

    # =====================================================
    # Authorization Helpers
    # =====================================================

    @staticmethod
    def _get_complaint(
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

    @staticmethod
    def _is_assigned_officer(
        db: Session,
        complaint_id: int,
        user_id: int,
    ) -> bool:

        assignment = (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.complaint_id == complaint_id,
                ComplaintAssignment.officer_id == user_id,
                ComplaintAssignment.is_active == True,
            )
            .first()
        )

        return assignment is not None

    @staticmethod
    def _authorize_complaint_access(
        db: Session,
        complaint: Complaint,
        current_user: User,
    ):

        # -------------------------------------------------
        # Admin
        # -------------------------------------------------

        if current_user.role == UserRole.ADMIN.value:
            return

        # -------------------------------------------------
        # Citizen
        # -------------------------------------------------

        if current_user.role == UserRole.CITIZEN.value:

            if complaint.citizen_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only access your own complaints.",
                )

            return

        # -------------------------------------------------
        # Officer
        # -------------------------------------------------

        if current_user.role == UserRole.OFFICER.value:

            if not ComplaintService._is_assigned_officer(
                db=db,
                complaint_id=complaint.id,
                user_id=current_user.id,
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "You can only access complaints "
                        "assigned to you."
                    ),
                )

            return

        # -------------------------------------------------
        # Department Head
        # -------------------------------------------------

        if current_user.role == UserRole.DEPARTMENT_HEAD.value:

            if (
                current_user.department_id is None
                or complaint.department_id
                != current_user.department_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "You can only access complaints "
                        "belonging to your department."
                    ),
                )

            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )

    # =====================================================
    # Status Authorization
    # =====================================================

    @staticmethod
    def _authorize_status_change(
        db: Session,
        complaint: Complaint,
        current_user: User,
        new_status: ComplaintStatus,
    ):

        # -------------------------------------------------
        # Admin
        # -------------------------------------------------

        if current_user.role == UserRole.ADMIN.value:
            return

        # -------------------------------------------------
        # Citizen
        # -------------------------------------------------

        if current_user.role == UserRole.CITIZEN.value:

            if complaint.citizen_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "You can only change the status "
                        "of your own complaints."
                    ),
                )

            if new_status != ComplaintStatus.REOPENED:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "Citizens can only reopen "
                        "their resolved complaints."
                    ),
                )

            if complaint.status != ComplaintStatus.RESOLVED:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Only resolved complaints "
                        "can be reopened."
                    ),
                )

            return

        # -------------------------------------------------
        # Officer
        # -------------------------------------------------

        if current_user.role == UserRole.OFFICER.value:

            if not ComplaintService._is_assigned_officer(
                db=db,
                complaint_id=complaint.id,
                user_id=current_user.id,
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "Only the assigned officer can "
                        "change this complaint status."
                    ),
                )

            allowed_statuses = {
                ComplaintStatus.IN_PROGRESS,
                ComplaintStatus.RESOLVED,
            }

            if new_status not in allowed_statuses:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "Officers can only move assigned "
                        "complaints to in-progress or resolved."
                    ),
                )

            return

        # -------------------------------------------------
        # Department Head
        # -------------------------------------------------

        if current_user.role == UserRole.DEPARTMENT_HEAD.value:

            if (
                current_user.department_id is None
                or complaint.department_id
                != current_user.department_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "You can only manage complaints "
                        "belonging to your department."
                    ),
                )

            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )

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

        sla_due_at = datetime.utcnow() + timedelta(
            hours=sla_hours
        )

        complaint = Complaint(
            title=complaint_data.title,
            description=complaint_data.description,
            location=complaint_data.location,
            status=ComplaintStatus.PENDING,
            priority=complaint_data.priority,
            citizen_id=citizen_id,
            department_id=complaint_data.department_id,
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
    def get_all_complaints(
        db: Session,
        current_user: User,
    ):

        query = (
            db.query(Complaint)
            .filter(
                Complaint.is_active == True,
            )
        )

        # -------------------------------------------------
        # Admin → All Complaints
        # -------------------------------------------------

        if current_user.role == UserRole.ADMIN.value:
            pass

        # -------------------------------------------------
        # Department Head → Own Department
        # -------------------------------------------------

        elif (
            current_user.role
            == UserRole.DEPARTMENT_HEAD.value
        ):

            query = query.filter(
                Complaint.department_id
                == current_user.department_id
            )

        # -------------------------------------------------
        # Officer → Assigned Complaints
        # -------------------------------------------------

        elif current_user.role == UserRole.OFFICER.value:

            query = query.join(
                ComplaintAssignment,
                ComplaintAssignment.complaint_id
                == Complaint.id,
            ).filter(
                ComplaintAssignment.officer_id
                == current_user.id,
                ComplaintAssignment.is_active == True,
            )

        # -------------------------------------------------
        # Citizen → Own Complaints
        # -------------------------------------------------

        elif current_user.role == UserRole.CITIZEN.value:

            query = query.filter(
                Complaint.citizen_id == current_user.id
            )

        else:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied.",
            )

        return (
            query
            .order_by(Complaint.id)
            .all()
        )

    # =====================================================
    # Get My Complaints
    # =====================================================

    @staticmethod
    def get_my_complaints(
        db: Session,
        citizen_id: int,
    ):

        return (
            db.query(Complaint)
            .filter(
                Complaint.citizen_id == citizen_id,
                Complaint.is_active == True,
            )
            .order_by(Complaint.id.desc())
            .all()
        )

    # =====================================================
    # Get My Complaint By ID
    # =====================================================

    @staticmethod
    def get_my_complaint_by_id(
        db: Session,
        complaint_id: int,
        citizen_id: int,
    ):

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

        return complaint

    # =====================================================
    # Get All Complaints SLA Details
    # =====================================================

    @staticmethod
    def get_all_complaints_sla(
        db: Session,
        current_user: User,
    ):

        complaints = ComplaintService.get_all_complaints(
            db=db,
            current_user=current_user,
        )

        result = []

        for complaint in complaints:

            result.append(
                ComplaintSLAResponse(
                    id=complaint.id,
                    title=complaint.title,
                    status=complaint.status,
                    priority=complaint.priority,
                    citizen_id=complaint.citizen_id,
                    department_id=complaint.department_id,
                    sla_hours=complaint.sla_hours,
                    sla_due_at=complaint.sla_due_at,
                    is_sla_breached=SLAUtils.is_breached(
                        complaint.sla_due_at
                    ),
                    remaining_hours=round(
                        SLAUtils.get_remaining_hours(
                            complaint.sla_due_at
                        ),
                        2,
                    ),
                    sla_status=SLAUtils.get_sla_status(
                        complaint.sla_due_at
                    ),
                )
            )

        return result

    # =====================================================
    # Get Near Breach Complaints
    # =====================================================

    @staticmethod
    def get_near_breach_complaints(
        db: Session,
        current_user: User,
    ):

        complaints = ComplaintService.get_all_complaints(
            db=db,
            current_user=current_user,
        )

        result = []

        for complaint in complaints:

            if SLAUtils.is_near_breach(
                complaint.sla_due_at
            ):

                result.append(
                    ComplaintSLAResponse(
                        id=complaint.id,
                        title=complaint.title,
                        status=complaint.status,
                        priority=complaint.priority,
                        citizen_id=complaint.citizen_id,
                        department_id=complaint.department_id,
                        sla_hours=complaint.sla_hours,
                        sla_due_at=complaint.sla_due_at,
                        is_sla_breached=False,
                        remaining_hours=round(
                            SLAUtils.get_remaining_hours(
                                complaint.sla_due_at
                            ),
                            2,
                        ),
                        sla_status="Near Breach",
                    )
                )

        return result

    # =====================================================
    # Get Breached Complaints
    # =====================================================

    @staticmethod
    def get_breached_complaints(
        db: Session,
        current_user: User,
    ):

        complaints = ComplaintService.get_all_complaints(
            db=db,
            current_user=current_user,
        )

        result = []

        for complaint in complaints:

            if SLAUtils.is_breached(
                complaint.sla_due_at
            ):

                result.append(
                    ComplaintSLAResponse(
                        id=complaint.id,
                        title=complaint.title,
                        status=complaint.status,
                        priority=complaint.priority,
                        citizen_id=complaint.citizen_id,
                        department_id=complaint.department_id,
                        sla_hours=complaint.sla_hours,
                        sla_due_at=complaint.sla_due_at,
                        is_sla_breached=True,
                        remaining_hours=round(
                            SLAUtils.get_remaining_hours(
                                complaint.sla_due_at
                            ),
                            2,
                        ),
                        sla_status="Breached",
                    )
                )

        return result

    # =====================================================
    # Get Complaint By ID
    # =====================================================

    @staticmethod
    def get_complaint_by_id(
        db: Session,
        complaint_id: int,
        current_user: User,
    ):

        complaint = ComplaintService._get_complaint(
            db=db,
            complaint_id=complaint_id,
        )

        ComplaintService._authorize_complaint_access(
            db=db,
            complaint=complaint,
            current_user=current_user,
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
        current_user: User,
    ):

        complaint = ComplaintService._get_complaint(
            db=db,
            complaint_id=complaint_id,
        )

        # -------------------------------------------------
        # Only Admin Can Edit General Fields
        # -------------------------------------------------

        if current_user.role != UserRole.ADMIN.value:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only admins can update "
                    "general complaint details."
                ),
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
        current_user: User,
    ):

        complaint = ComplaintService._get_complaint(
            db=db,
            complaint_id=complaint_id,
        )

        current_status = ComplaintStatus(
            complaint.status
        )

        old_status = current_status
        new_status = status_data.status

        # -------------------------------------------------
        # Role / Ownership Authorization
        # -------------------------------------------------

        ComplaintService._authorize_status_change(
            db=db,
            complaint=complaint,
            current_user=current_user,
            new_status=new_status,
        )

        # -------------------------------------------------
        # Status Transition Validation
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Update Status
        # -------------------------------------------------

        complaint.status = new_status

        # -------------------------------------------------
        # Create History
        # -------------------------------------------------

        ComplaintHistoryService.create_history(
            db=db,
            complaint_id=complaint.id,
            old_status=old_status,
            new_status=new_status,
            changed_by=current_user.id,
            remarks=(
                f"Status changed from "
                f"{old_status.value} to "
                f"{new_status.value}"
            ),
        )

        # -------------------------------------------------
        # Create Citizen Notification
        # -------------------------------------------------

        notification = Notification(
            user_id=complaint.citizen_id,
            complaint_id=complaint.id,
            escalation_id=None,
            title="Complaint Status Updated",
            message=(
                f"Your complaint #{complaint.id} status has been "
                f"changed from {old_status.value} to "
                f"{new_status.value}."
            ),
            notification_type="COMPLAINT_STATUS_UPDATED",
            is_read=False,
            is_active=True,
        )

        db.add(notification)

        # -------------------------------------------------
        # Commit Status + History + Notification Together
        # -------------------------------------------------

        db.commit()

        db.refresh(complaint)

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