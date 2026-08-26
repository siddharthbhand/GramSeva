from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.core.user_roles import UserRole


class AuthService:

    # =====================================================
    # Register User
    # =====================================================

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserRegister,
    ):

        # -------------------------------------------------
        # Check Existing Email
        # -------------------------------------------------

        existing_email = (
            db.query(User)
            .filter(
                User.email == user_data.email,
            )
            .first()
        )

        if existing_email:
            raise ValueError(
                "Email already registered."
            )

        # -------------------------------------------------
        # Check Existing Phone
        # -------------------------------------------------

        existing_phone = (
            db.query(User)
            .filter(
                User.phone == user_data.phone,
            )
            .first()
        )

        if existing_phone:
            raise ValueError(
                "Phone number already registered."
            )

        # -------------------------------------------------
        # Hash Password
        # -------------------------------------------------

        hashed_password = hash_password(
            user_data.password
        )

        # -------------------------------------------------
        # Create User
        # -------------------------------------------------
        # Public registration always creates a citizen.
        # Admin/officer/department-head accounts must be
        # managed through authorized admin operations.

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password=hashed_password,
            role=UserRole.CITIZEN.value,
            department_id=None,
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return new_user

    # =====================================================
    # Login User
    # =====================================================

    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str,
    ):

        # -------------------------------------------------
        # Find User
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(
                User.email == email,
            )
            .first()
        )

        if not user:
            raise ValueError(
                "Invalid email or password."
            )

        # -------------------------------------------------
        # Verify Password
        # -------------------------------------------------

        if not verify_password(
            password,
            user.password,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        # -------------------------------------------------
        # Check Active Account
        # -------------------------------------------------

        if not user.is_active:
            raise ValueError(
                "User account is inactive."
            )

        # -------------------------------------------------
        # Create JWT Token
        # -------------------------------------------------

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "role": user.role,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }