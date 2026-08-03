from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import ComplaintStatus


# =====================================================
# Complaint History Response
# =====================================================

class ComplaintHistoryResponse(BaseModel):

    id: int

    complaint_id: int

    old_status: ComplaintStatus

    new_status: ComplaintStatus

    changed_by: int

    remarks: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Complaint History List Response
# =====================================================

class ComplaintHistoryListResponse(BaseModel):

    id: int

    old_status: ComplaintStatus

    new_status: ComplaintStatus

    changed_by: int

    remarks: str | None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )