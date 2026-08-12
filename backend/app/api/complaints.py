from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
    ComplaintListResponse,
    ComplaintStatusUpdate,
    ComplaintSLAResponse,
)

from app.services.complaint_service import ComplaintService


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)


# =====================================================
# Create Complaint
# =====================================================

@router.post(
    "/",
    response_model=ComplaintResponse,
)
def create_complaint(
    complaint_data: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ComplaintService.create_complaint(
        db=db,
        complaint_data=complaint_data,
        citizen_id=current_user.id,
    )


# =====================================================
# Get All Complaints
# =====================================================

@router.get(
    "/",
    response_model=List[ComplaintListResponse],
)
def get_all_complaints(
    db: Session = Depends(get_db),
):
    return ComplaintService.get_all_complaints(db)


# =====================================================
# Get My Complaints
# =====================================================

@router.get(
    "/my",
    response_model=List[ComplaintListResponse],
)
def get_my_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ComplaintService.get_my_complaints(
        db=db,
        citizen_id=current_user.id,
    )


# =====================================================
# Get My Complaint By ID
# =====================================================

@router.get(
    "/my/{complaint_id}",
    response_model=ComplaintResponse,
)
def get_my_complaint_by_id(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ComplaintService.get_my_complaint_by_id(
        db=db,
        complaint_id=complaint_id,
        citizen_id=current_user.id,
    )


# =====================================================
# Get All Complaints SLA Details
# =====================================================

@router.get(
    "/sla",
    response_model=List[ComplaintSLAResponse],
)
def get_all_complaints_sla(
    db: Session = Depends(get_db),
):
    return ComplaintService.get_all_complaints_sla(db)


# =====================================================
# Get Near Breach Complaints
# =====================================================

@router.get(
    "/near-breach",
    response_model=List[ComplaintSLAResponse],
)
def get_near_breach_complaints(
    db: Session = Depends(get_db),
):
    return ComplaintService.get_near_breach_complaints(db)


# =====================================================
# Get Breached Complaints
# =====================================================

@router.get(
    "/breached",
    response_model=List[ComplaintSLAResponse],
)
def get_breached_complaints(
    db: Session = Depends(get_db),
):
    return ComplaintService.get_breached_complaints(db)


# =====================================================
# Get Complaint By ID
# =====================================================

@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def get_complaint_by_id(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    return ComplaintService.get_complaint_by_id(
        db,
        complaint_id,
    )


# =====================================================
# Update Complaint
# =====================================================

@router.put(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def update_complaint(
    complaint_id: int,
    complaint_data: ComplaintUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintService.update_complaint(
        db,
        complaint_id,
        complaint_data,
    )


# =====================================================
# Update Complaint Status
# =====================================================

@router.put(
    "/{complaint_id}/status",
    response_model=ComplaintResponse,
)
def update_complaint_status(
    complaint_id: int,
    status_data: ComplaintStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return ComplaintService.update_complaint_status(
        db=db,
        complaint_id=complaint_id,
        status_data=status_data,
        changed_by=current_user.id,
    )


# =====================================================
# Delete Complaint
# =====================================================

@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintService.delete_complaint(
        db,
        complaint_id,
    )