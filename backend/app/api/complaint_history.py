from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.complaint_history import (
    ComplaintHistoryResponse,
    ComplaintHistoryListResponse,
)

from app.services.complaint_history_service import (
    ComplaintHistoryService,
)


router = APIRouter(
    prefix="/complaint-history",
    tags=["Complaint History"],
)


# =====================================================
# Get Complaint History
# =====================================================

@router.get(
    "/complaint/{complaint_id}",
    response_model=List[ComplaintHistoryListResponse],
)
def get_complaint_history(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ComplaintHistoryService.get_complaint_history(
        db=db,
        complaint_id=complaint_id,
        citizen_id=current_user.id,
    )


# =====================================================
# Get History By ID
# =====================================================

@router.get(
    "/{history_id}",
    response_model=ComplaintHistoryResponse,
)
def get_history_by_id(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ComplaintHistoryService.get_history_by_id(
        db=db,
        history_id=history_id,
        citizen_id=current_user.id,
    )