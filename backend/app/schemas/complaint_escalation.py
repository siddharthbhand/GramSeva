from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Create Escalation
# =====================================================

class ComplaintEscalationCreate(BaseModel):
    complaint_id: int
    escalated_to: Optional[int] = None
    reason: str
    remarks: Optional[str] = None


# =====================================================
# Update Escalation
# =====================================================

class ComplaintEscalationUpdate(BaseModel):
    escalation_level: int
    escalated_to: Optional[int] = None
    reason: str
    remarks: Optional[str] = None
    is_active: bool


# =====================================================
# Response
# =====================================================

class ComplaintEscalationResponse(BaseModel):
    id: int
    complaint_id: int
    escalation_level: int
    escalated_to: Optional[int]
    escalated_by: Optional[int]
    reason: str
    remarks: Optional[str]
    is_active: bool
    escalated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# List Response
# =====================================================

class ComplaintEscalationListResponse(BaseModel):
    id: int
    complaint_id: int
    escalation_level: int
    escalated_to: Optional[int]
    escalated_at: datetime
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )