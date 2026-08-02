from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.department import Department
from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
)


class ComplaintService:

    @staticmethod
    def create_complaint(
        db: Session,
        complaint_data: ComplaintCreate,
        citizen_id: int,
    ):
        # Validate Department
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

        complaint = Complaint(
            title=complaint_data.title,
            description=complaint_data.description,
            location=complaint_data.location,
            priority=complaint_data.priority,
            citizen_id=citizen_id,
            department_id=complaint_data.department_id,
        )

        db.add(complaint)
        db.commit()
        db.refresh(complaint)

        return complaint

    @staticmethod
    def get_all_complaints(db: Session):

        return (
            db.query(Complaint)
            .filter(Complaint.is_active == True)
            .order_by(Complaint.id)
            .all()
        )

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

    @staticmethod
    def update_complaint(
        db: Session,
        complaint_id: int,
        complaint_data: ComplaintUpdate,
    ):

        complaint = (
            db.query(Complaint)
            .filter(Complaint.id == complaint_id)
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

    @staticmethod
    def delete_complaint(
        db: Session,
        complaint_id: int,
    ):

        complaint = (
            db.query(Complaint)
            .filter(Complaint.id == complaint_id)
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