from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ComplaintAssignmentCreate(BaseModel):
    complaint_id: int
    officer_id: int
    remarks: Optional[str] = None


class ComplaintAssignmentUpdate(BaseModel):
    officer_id: Optional[int] = None
    remarks: Optional[str] = None
    is_active: Optional[bool] = None


class ComplaintAssignmentResponse(BaseModel):
    id: int
    complaint_id: int
    officer_id: int
    assigned_by: int
    remarks: Optional[str]
    is_active: bool
    assigned_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ComplaintAssignmentListResponse(BaseModel):
    id: int
    complaint_id: int
    officer_id: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )