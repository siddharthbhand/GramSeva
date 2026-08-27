from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.models.department import Department
from app.models.notification import Notification
from app.models.user import User

from app.schemas.complaint_assignment import (
    ComplaintAssignmentCreate,
    ComplaintAssignmentUpdate,
)


class ComplaintAssignmentService:

    # =====================================================
    # Assign Complaint
    # =====================================================

    @staticmethod
    def assign_complaint(
        db: Session,
        assignment_data: ComplaintAssignmentCreate,
        assigned_by: int,
    ):

        # -------------------------------------------------
        # Check Complaint
        # -------------------------------------------------

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == assignment_data.complaint_id,
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
        # Check Officer Exists and Is Active
        # -------------------------------------------------

        officer = (
            db.query(User)
            .filter(
                User.id == assignment_data.officer_id,
                User.is_active == True,
            )
            .first()
        )

        if not officer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Officer not found.",
            )

        # -------------------------------------------------
        # Validate Officer Role
        # -------------------------------------------------

        if officer.role != "officer":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected user is not an officer.",
            )

        # -------------------------------------------------
        # Validate Complaint Department
        # -------------------------------------------------

        if complaint.department_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Complaint must be assigned to a department "
                    "before assigning an officer."
                ),
            )

        # -------------------------------------------------
        # Check Complaint Department
        # -------------------------------------------------

        complaint_department = (
            db.query(Department)
            .filter(
                Department.id == complaint.department_id,
                Department.is_active == True,
            )
            .first()
        )

        if not complaint_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint department not found or inactive.",
            )

        # -------------------------------------------------
        # Validate Officer Department
        # -------------------------------------------------

        if officer.department_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Officer is not assigned to a department.",
            )

        # -------------------------------------------------
        # Check Officer Department
        # -------------------------------------------------

        officer_department = (
            db.query(Department)
            .filter(
                Department.id == officer.department_id,
                Department.is_active == True,
            )
            .first()
        )

        if not officer_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Officer department not found or inactive.",
            )

        # -------------------------------------------------
        # Validate Department Matching
        # -------------------------------------------------

        if complaint.department_id != officer.department_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Officer does not belong to the complaint's department."
                ),
            )

        # -------------------------------------------------
        # Prevent Duplicate Assignment
        # -------------------------------------------------

        existing_assignment = (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.complaint_id
                == assignment_data.complaint_id,
                ComplaintAssignment.is_active == True,
            )
            .first()
        )

        if existing_assignment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complaint is already assigned.",
            )

        # -------------------------------------------------
        # Create Assignment
        # -------------------------------------------------

        assignment = ComplaintAssignment(
            complaint_id=assignment_data.complaint_id,
            officer_id=assignment_data.officer_id,
            assigned_by=assigned_by,
            remarks=assignment_data.remarks,
        )

        db.add(assignment)

        # -------------------------------------------------
        # Create Assignment Notification
        # -------------------------------------------------

        notification = Notification(
            user_id=assignment_data.officer_id,
            complaint_id=assignment_data.complaint_id,
            escalation_id=None,
            title="Complaint Assigned",
            message=(
                f"Complaint #{assignment_data.complaint_id} "
                "has been assigned to you for further action."
            ),
            notification_type="COMPLAINT_ASSIGNED",
            is_read=False,
            is_active=True,
        )

        db.add(notification)

        # -------------------------------------------------
        # Commit Assignment + Notification Together
        # -------------------------------------------------

        db.commit()

        db.refresh(assignment)

        return assignment

    # =====================================================
    # Get All Assignments
    # =====================================================

    @staticmethod
    def get_all_assignments(
        db: Session,
    ):

        return (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.is_active == True,
            )
            .all()
        )

    # =====================================================
    # Get Assignment By ID
    # =====================================================

    @staticmethod
    def get_assignment_by_id(
        db: Session,
        assignment_id: int,
    ):

        assignment = (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.id == assignment_id,
                ComplaintAssignment.is_active == True,
            )
            .first()
        )

        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found.",
            )

        return assignment

    # =====================================================
    # Update / Reassign Assignment
    # =====================================================

    @staticmethod
    def update_assignment(
        db: Session,
        assignment_id: int,
        assignment_data: ComplaintAssignmentUpdate,
        assigned_by: int,
    ):

        # -------------------------------------------------
        # Get Existing Active Assignment
        # -------------------------------------------------

        assignment = (
            ComplaintAssignmentService.get_assignment_by_id(
                db,
                assignment_id,
            )
        )

        # -------------------------------------------------
        # Get Complaint
        # -------------------------------------------------

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.id == assignment.complaint_id,
                Complaint.is_active == True,
            )
            .first()
        )

        if not complaint:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Complaint not found.",
            )

        # =================================================
        # Reassignment
        # =================================================

        if assignment_data.officer_id is not None:

            # ---------------------------------------------
            # Check New Officer
            # ---------------------------------------------

            officer = (
                db.query(User)
                .filter(
                    User.id == assignment_data.officer_id,
                    User.is_active == True,
                )
                .first()
            )

            if not officer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Officer not found.",
                )

            # ---------------------------------------------
            # Validate Officer Role
            # ---------------------------------------------

            if officer.role != "officer":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Selected user is not an officer.",
                )

            # ---------------------------------------------
            # Complaint Must Have Department
            # ---------------------------------------------

            if complaint.department_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Complaint has no department assigned.",
                )

            # ---------------------------------------------
            # Validate Officer Department
            # ---------------------------------------------

            if officer.department_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Officer is not assigned to a department.",
                )

            # ---------------------------------------------
            # Check Officer Department Is Active
            # ---------------------------------------------

            officer_department = (
                db.query(Department)
                .filter(
                    Department.id == officer.department_id,
                    Department.is_active == True,
                )
                .first()
            )

            if not officer_department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Officer department not found or inactive.",
                )

            # ---------------------------------------------
            # Validate Same Department
            # ---------------------------------------------

            if officer.department_id != complaint.department_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Officer does not belong to the "
                        "complaint's department."
                    ),
                )

            # ---------------------------------------------
            # Prevent Same Officer Reassignment
            # ---------------------------------------------

            if officer.id == assignment.officer_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Complaint is already assigned to this officer."
                    ),
                )

            # ---------------------------------------------
            # Deactivate Previous Assignment
            # ---------------------------------------------

            assignment.is_active = False

            # ---------------------------------------------
            # Create New Assignment
            # ---------------------------------------------

            new_assignment = ComplaintAssignment(
                complaint_id=assignment.complaint_id,
                officer_id=officer.id,
                assigned_by=assigned_by,
                remarks=assignment_data.remarks,
            )

            db.add(new_assignment)

            # ---------------------------------------------
            # Create Reassignment Notification
            # ---------------------------------------------

            notification = Notification(
                user_id=officer.id,
                complaint_id=assignment.complaint_id,
                escalation_id=None,
                title="Complaint Reassigned",
                message=(
                    f"Complaint #{assignment.complaint_id} "
                    "has been reassigned to you for further action."
                ),
                notification_type="COMPLAINT_REASSIGNED",
                is_read=False,
                is_active=True,
            )

            db.add(notification)

            # ---------------------------------------------
            # Commit
            # ---------------------------------------------

            db.commit()

            db.refresh(new_assignment)

            return new_assignment

        # =================================================
        # Remarks / Active Status Update
        # =================================================

        if assignment_data.remarks is not None:
            assignment.remarks = assignment_data.remarks

        if assignment_data.is_active is not None:
            assignment.is_active = assignment_data.is_active

        db.commit()
        db.refresh(assignment)

        return assignment

    # =====================================================
    # Delete Assignment (Soft Delete)
    # =====================================================

    @staticmethod
    def delete_assignment(
        db: Session,
        assignment_id: int,
    ):

        assignment = (
            ComplaintAssignmentService.get_assignment_by_id(
                db,
                assignment_id,
            )
        )

        assignment.is_active = False

        db.commit()

        return {
            "message": "Assignment deleted successfully."
        }