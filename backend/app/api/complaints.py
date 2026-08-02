from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_admin
from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
    ComplaintListResponse,
)
from app.services.complaint_service import ComplaintService

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)


@router.post(
    "/",
    response_model=ComplaintResponse,
)
def create_complaint(
    complaint_data: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return ComplaintService.create_complaint(
        db=db,
        complaint_data=complaint_data,
        citizen_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[ComplaintListResponse],
)
def get_all_complaints(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return ComplaintService.get_all_complaints(db)


@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def get_complaint_by_id(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return ComplaintService.get_complaint_by_id(
        db,
        complaint_id,
    )


@router.put(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def update_complaint(
    complaint_id: int,
    complaint_data: ComplaintUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return ComplaintService.update_complaint(
        db=db,
        complaint_id=complaint_id,
        complaint_data=complaint_data,
    )


@router.delete(
    "/{complaint_id}",
)
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return ComplaintService.delete_complaint(
        db=db,
        complaint_id=complaint_id,
    )