from pydantic import BaseModel, ConfigDict

from app.core.enums import ComplaintStatus


class ComplaintCreate(BaseModel):
    title: str
    description: str
    location: str
    priority: str = "Medium"
    department_id: int | None = None


class ComplaintUpdate(BaseModel):
    title: str
    description: str
    location: str
    status: ComplaintStatus
    priority: str
    department_id: int | None = None
    is_active: bool


class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus


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

    model_config = ConfigDict(
        from_attributes=True,
    )


class ComplaintListResponse(BaseModel):
    id: int
    title: str
    status: ComplaintStatus
    priority: str
    citizen_id: int
    department_id: int | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )