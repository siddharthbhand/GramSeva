from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
)


class DepartmentService:

    @staticmethod
    def create_department(
        db: Session,
        department_data: DepartmentCreate,
    ):
        existing_department = (
            db.query(Department)
            .filter(
                Department.name == department_data.name
            )
            .first()
        )

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department already exists."
            )

        department = Department(
            name=department_data.name,
            description=department_data.description,
        )

        db.add(department)
        db.commit()
        db.refresh(department)

        return department

    @staticmethod
    def get_all_departments(
        db: Session,
    ):
        return (
            db.query(Department)
            .order_by(Department.id)
            .all()
        )

    @staticmethod
    def get_department_by_id(
        db: Session,
        department_id: int,
    ):
        department = (
            db.query(Department)
            .filter(
                Department.id == department_id
            )
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found."
            )

        return department

    @staticmethod
    def update_department(
        db: Session,
        department_id: int,
        department_data: DepartmentUpdate,
    ):
        department = (
            db.query(Department)
            .filter(
                Department.id == department_id
            )
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found."
            )

        existing_department = (
            db.query(Department)
            .filter(
                Department.name == department_data.name,
                Department.id != department_id,
            )
            .first()
        )

        if existing_department:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department already exists."
            )

        department.name = department_data.name
        department.description = department_data.description
        department.is_active = department_data.is_active

        db.commit()
        db.refresh(department)

        return department

    @staticmethod
    def delete_department(
        db: Session,
        department_id: int,
    ):
        department = (
            db.query(Department)
            .filter(
                Department.id == department_id
            )
            .first()
        )

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found."
            )

        if not department.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department is already deactivated."
            )

        department.is_active = False

        db.commit()
        db.refresh(department)

        return {
            "message": "Department deactivated successfully."
        }