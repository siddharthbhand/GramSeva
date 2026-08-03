from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.complaint_assignment import ComplaintAssignment
from app.models.user import User
from app.schemas.complaint_assignment import ComplaintAssignmentCreate


class ComplaintAssignmentService:

    @staticmethod
    def assign_complaint(
        db: Session,
        assignment_data: ComplaintAssignmentCreate,
        assigned_by: int,
    ):

        # ----------------------------
        # Check Complaint
        # ----------------------------

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

        # ----------------------------
        # Check Officer
        # ----------------------------

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

        # ----------------------------
        # Prevent Duplicate Assignment
        # ----------------------------

        existing_assignment = (
            db.query(ComplaintAssignment)
            .filter(
                ComplaintAssignment.complaint_id == assignment_data.complaint_id,
                ComplaintAssignment.is_active == True,
            )
            .first()
        )

        if existing_assignment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complaint is already assigned.",
            )

        # ----------------------------
        # Create Assignment
        # ----------------------------

        assignment = ComplaintAssignment(
            complaint_id=assignment_data.complaint_id,
            officer_id=assignment_data.officer_id,
            assigned_by=assigned_by,
            remarks=assignment_data.remarks,
        )

        db.add(assignment)
        db.commit()
        db.refresh(assignment)

        return assignment

    # =====================================================
    # Get All Assignments
    # =====================================================

    @staticmethod
    def get_all_assignments(db: Session):

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
    # Update Assignment
    # =====================================================

    @staticmethod
    def update_assignment(
        db: Session,
        assignment_id: int,
        remarks: str,
    ):

        assignment = ComplaintAssignmentService.get_assignment_by_id(
            db,
            assignment_id,
        )

        assignment.remarks = remarks

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

        assignment = ComplaintAssignmentService.get_assignment_by_id(
            db,
            assignment_id,
        )

        assignment.is_active = False

        db.commit()

        return {
            "message": "Assignment deleted successfully."
        }