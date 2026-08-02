from pydantic import BaseModel, ConfigDict
from typing import Optional


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class DepartmentListResponse(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )