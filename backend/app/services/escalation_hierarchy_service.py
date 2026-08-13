from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.core.user_roles import UserRole
from app.models.complaint_escalation import ComplaintEscalation
from app.models.user import User


class EscalationHierarchyService:

    # =====================================================
    # Escalation Hierarchy
    # =====================================================

    ESCALATION_HIERARCHY = {
        1: UserRole.DEPARTMENT_HEAD.value,
        2: UserRole.ADMIN.value,
    }

    # =====================================================
    # Get Next Escalation Level
    # =====================================================

    @staticmethod
    def get_next_escalation_level(
        db: Session,
        complaint_id: int,
    ) -> Optional[int]:
        """
        Return the next escalation level for a complaint.

        Level 1 -> Department Head
        Level 2 -> Admin

        Returns None when the maximum escalation level
        has already been reached.
        """

        latest_escalation = (
            db.query(ComplaintEscalation)
            .filter(
                ComplaintEscalation.complaint_id
                == complaint_id,
                ComplaintEscalation.is_active == True,
            )
            .order_by(
                ComplaintEscalation.escalation_level.desc(),
                ComplaintEscalation.id.desc(),
            )
            .first()
        )

        # -------------------------------------------------
        # First escalation
        # -------------------------------------------------

        if latest_escalation is None:
            return 1

        next_level = (
            latest_escalation.escalation_level + 1
        )

        # -------------------------------------------------
        # Maximum escalation level reached
        # -------------------------------------------------

        if next_level not in EscalationHierarchyService.ESCALATION_HIERARCHY:
            return None

        return next_level

    # =====================================================
    # Get Role For Escalation Level
    # =====================================================

    @staticmethod
    def get_target_role(
        escalation_level: int,
    ) -> Optional[str]:
        """
        Return the user role associated with an
        escalation level.
        """

        return (
            EscalationHierarchyService
            .ESCALATION_HIERARCHY
            .get(escalation_level)
        )

    # =====================================================
    # Find Escalation Target
    # =====================================================

    @staticmethod
    def get_escalation_target(
        db: Session,
        escalation_level: int,
    ) -> Optional[User]:
        """
        Find an active user who is eligible to receive
        the escalation for the requested level.

        Level 1 -> Department Head
        Level 2 -> Admin
        """

        target_role = (
            EscalationHierarchyService.get_target_role(
                escalation_level
            )
        )

        if target_role is None:
            return None

        target_user = (
            db.query(User)
            .filter(
                User.role == target_role,
                User.is_active == True,
            )
            .order_by(
                User.id.asc()
            )
            .first()
        )

        return target_user

    # =====================================================
    # Get Next Escalation Target
    # =====================================================

    @staticmethod
    def get_next_escalation_target(
        db: Session,
        complaint_id: int,
    ) -> Tuple[
        Optional[int],
        Optional[User],
    ]:
        """
        Determine both the next escalation level and
        the user who should receive the escalation.

        Returns:

            (
                escalation_level,
                target_user
            )

        If no further escalation is possible:

            (
                None,
                None
            )
        """

        next_level = (
            EscalationHierarchyService
            .get_next_escalation_level(
                db=db,
                complaint_id=complaint_id,
            )
        )

        if next_level is None:
            return None, None

        target_user = (
            EscalationHierarchyService
            .get_escalation_target(
                db=db,
                escalation_level=next_level,
            )
        )

        if target_user is None:
            return next_level, None

        return next_level, target_user

    # =====================================================
    # Validate Escalation Target
    # =====================================================

    @staticmethod
    def is_valid_escalation_target(
        user: Optional[User],
        escalation_level: int,
    ) -> bool:
        """
        Validate whether a user is eligible to receive
        an escalation at the requested level.
        """

        if user is None:
            return False

        if not user.is_active:
            return False

        expected_role = (
            EscalationHierarchyService
            .get_target_role(
                escalation_level
            )
        )

        if expected_role is None:
            return False

        return user.role == expected_role

    # =====================================================
    # Get Hierarchy Information
    # =====================================================

    @staticmethod
    def get_hierarchy() -> dict:
        """
        Return the configured escalation hierarchy.
        """

        return {
            "1": UserRole.DEPARTMENT_HEAD.value,
            "2": UserRole.ADMIN.value,
        }