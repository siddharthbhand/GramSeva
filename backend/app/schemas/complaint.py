from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import ComplaintStatus


# =====================================================
# Create Complaint
# =====================================================

class ComplaintCreate(BaseModel):
    title: str
    description: str
    location: str
    priority: str = "Medium"
    department_id: int | None = None


# =====================================================
# Update Complaint
# =====================================================

class ComplaintUpdate(BaseModel):
    """
    Update general complaint information.

    Status is intentionally excluded.
    Status changes must use the dedicated status endpoint
    so that transition and role authorization rules apply.
    """

    title: str
    description: str
    location: str
    priority: str
    department_id: int | None = None
    is_active: bool


# =====================================================
# Update Complaint Status
# =====================================================

class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus


# =====================================================
# Complaint Response
# =====================================================

class ComplaintResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    status: ComplaintStatus
    priority: str
    citizen_id: int
    department_id: int | None
    is_active: bool

    # ==========================
    # SLA Fields
    # ==========================

    sla_hours: int
    sla_due_at: datetime | None
    is_sla_breached: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Complaint List Response
# =====================================================

class ComplaintListResponse(BaseModel):
    id: int
    title: str
    status: ComplaintStatus
    priority: str
    citizen_id: int
    department_id: int | None
    is_active: bool

    # ==========================
    # SLA Fields
    # ==========================

    sla_hours: int
    sla_due_at: datetime | None
    is_sla_breached: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Complaint SLA Response
# =====================================================

class ComplaintSLAResponse(BaseModel):
    id: int
    title: str
    status: ComplaintStatus
    priority: str
    citizen_id: int
    department_id: int | None

    sla_hours: int
    sla_due_at: datetime | None
    is_sla_breached: bool

    remaining_hours: float
    sla_status: str

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Complaint SLA List Response
# =====================================================

class ComplaintSLAListResponse(BaseModel):
    complaints: list[ComplaintSLAResponse]