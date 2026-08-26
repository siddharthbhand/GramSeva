from pydantic import BaseModel, EmailStr, Field

from app.core.user_roles import UserRole


# =====================================================
# User Update
# =====================================================

class UserUpdate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
    )

    role: UserRole

    department_id: int | None = None

    is_active: bool


# =====================================================
# User List Response
# =====================================================

class UserListResponse(BaseModel):
    id: int

    full_name: str

    email: EmailStr

    phone: str

    role: str

    department_id: int | None

    is_active: bool

    model_config = {
        "from_attributes": True,
    }