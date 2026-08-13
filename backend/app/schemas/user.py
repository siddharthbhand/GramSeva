from pydantic import BaseModel, EmailStr, Field

from app.core.user_roles import UserRole


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

    is_active: bool


class UserListResponse(BaseModel):
    id: int

    full_name: str

    email: EmailStr

    phone: str

    role: str

    is_active: bool

    model_config = {
        "from_attributes": True
    }