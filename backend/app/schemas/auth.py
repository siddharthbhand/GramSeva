from pydantic import BaseModel, EmailStr, Field

from app.core.user_roles import UserRole


class UserRegister(BaseModel):
    """
    Schema for user registration.
    """

    full_name: str = Field(..., min_length=3, max_length=100)

    email: EmailStr

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
    )

    password: str = Field(
        ...,
        min_length=8,
    )

    role: UserRole = Field(
        default=UserRole.CITIZEN,
    )


class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    email: EmailStr

    password: str


class UserResponse(BaseModel):
    """
    Schema returned after successful registration.
    """

    id: int

    full_name: str

    email: EmailStr

    role: str

    model_config = {
        "from_attributes": True
    }