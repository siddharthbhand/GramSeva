from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentListResponse,
)
from app.services.department_service import DepartmentService

router = APIRouter()


@router.post(
    "/",
    response_model=DepartmentResponse,
)
def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return DepartmentService.create_department(
        db,
        department_data,
    )


@router.get(
    "/",
    response_model=List[DepartmentListResponse],
)
def get_all_departments(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return DepartmentService.get_all_departments(db)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def get_department_by_id(
    department_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return DepartmentService.get_department_by_id(
        db,
        department_id,
    )


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse,
)
def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return DepartmentService.update_department(
        db,
        department_id,
        department_data,
    )


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return DepartmentService.delete_department(
        db,
        department_id,
    )