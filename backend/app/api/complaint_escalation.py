from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin

from app.models.user import User

from app.schemas.complaint_escalation import (
    ComplaintEscalationCreate,
    ComplaintEscalationUpdate,
    ComplaintEscalationResponse,
    ComplaintEscalationListResponse,
)

from app.services.complaint_escalation_service import (
    ComplaintEscalationService,
)


router = APIRouter(
    prefix="/complaint-escalations",
    tags=["Complaint Escalations"],
)


# =====================================================
# Get All Escalations
# =====================================================

@router.get(
    "/",
    response_model=List[ComplaintEscalationListResponse],
)
def get_all_escalations(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintEscalationService.get_all_escalations(
        db=db,
    )


# =====================================================
# Create Complaint Escalation
# =====================================================

@router.post(
    "/",
    response_model=ComplaintEscalationResponse,
)
def create_escalation(
    escalation_data: ComplaintEscalationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return ComplaintEscalationService.create_escalation(
        db=db,
        escalation_data=escalation_data,
        escalated_by=current_user.id,
    )


# =====================================================
# Automatic SLA Escalation
# =====================================================

@router.post(
    "/auto/{complaint_id}",
    response_model=ComplaintEscalationResponse,
)
def auto_escalate_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintEscalationService.auto_escalate_complaint(
        db=db,
        complaint_id=complaint_id,
    )


# =====================================================
# Get Escalations By Complaint
# =====================================================

@router.get(
    "/complaint/{complaint_id}",
    response_model=List[ComplaintEscalationResponse],
)
def get_escalations_by_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintEscalationService.get_escalations_by_complaint(
        db=db,
        complaint_id=complaint_id,
    )


# =====================================================
# Get Escalation By ID
# =====================================================

@router.get(
    "/{escalation_id}",
    response_model=ComplaintEscalationResponse,
)
def get_escalation_by_id(
    escalation_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintEscalationService.get_escalation_by_id(
        db=db,
        escalation_id=escalation_id,
    )


# =====================================================
# Update Escalation
# =====================================================

@router.put(
    "/{escalation_id}",
    response_model=ComplaintEscalationResponse,
)
def update_escalation(
    escalation_id: int,
    escalation_data: ComplaintEscalationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintEscalationService.update_escalation(
        db=db,
        escalation_id=escalation_id,
        escalation_data=escalation_data,
    )


# =====================================================
# Delete Escalation
# =====================================================

@router.delete(
    "/{escalation_id}"
)
def delete_escalation(
    escalation_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ComplaintEscalationService.delete_escalation(
        db=db,
        escalation_id=escalation_id,
    )