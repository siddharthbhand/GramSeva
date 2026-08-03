from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.complaint_assignment import (
    ComplaintAssignmentCreate,
    ComplaintAssignmentResponse,
)
from app.services.complaint_assignment_service import (
    ComplaintAssignmentService,
)

router = APIRouter(
    prefix="/assignments",
    tags=["Complaint Assignments"],
)


@router.post(
    "/",
    response_model=ComplaintAssignmentResponse,
)
def assign_complaint(
    assignment_data: ComplaintAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return ComplaintAssignmentService.assign_complaint(
        db=db,
        assignment_data=assignment_data,
        assigned_by=current_user.id,
    )


@router.get(
    "/",
    response_model=List[ComplaintAssignmentResponse],
)
def get_all_assignments(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintAssignmentService.get_all_assignments(db)


@router.get(
    "/{assignment_id}",
    response_model=ComplaintAssignmentResponse,
)
def get_assignment_by_id(
    assignment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintAssignmentService.get_assignment_by_id(
        db,
        assignment_id,
    )


@router.put(
    "/{assignment_id}",
    response_model=ComplaintAssignmentResponse,
)
def update_assignment(
    assignment_id: int,
    remarks: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintAssignmentService.update_assignment(
        db,
        assignment_id,
        remarks,
    )


@router.delete("/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintAssignmentService.delete_assignment(
        db,
        assignment_id,
    )