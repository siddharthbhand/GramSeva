from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.department import Department
from app.schemas.user import UserUpdate
from app.core.user_roles import UserRole


class UserService:

    # =====================================================
    # Get All Users
    # =====================================================

    @staticmethod
    def get_all_users(
        db: Session,
    ):
        return (
            db.query(User)
            .order_by(User.id)
            .all()
        )

    # =====================================================
    # Get User By ID
    # =====================================================

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: int,
    ):
        user = (
            db.query(User)
            .filter(
                User.id == user_id,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return user

    # =====================================================
    # Update User
    # =====================================================

    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        user_data: UserUpdate,
    ):
        user = (
            db.query(User)
            .filter(
                User.id == user_id,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        # -------------------------------------------------
        # Check Duplicate Phone
        # -------------------------------------------------

        existing_phone = (
            db.query(User)
            .filter(
                User.phone == user_data.phone,
                User.id != user_id,
            )
            .first()
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already exists.",
            )

        # -------------------------------------------------
        # Validate Department Based On Role
        # -------------------------------------------------

        role = user_data.role

        # Officers and Department Heads must belong
        # to an active department.
        if role in (
            UserRole.OFFICER,
            UserRole.DEPARTMENT_HEAD,
        ):
            if user_data.department_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Department is required for "
                        "officer and department head roles."
                    ),
                )

            department = (
                db.query(Department)
                .filter(
                    Department.id == user_data.department_id,
                    Department.is_active == True,
                )
                .first()
            )

            if not department:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Active department not found.",
                )

        # -------------------------------------------------
        # Citizen and Admin should not be attached
        # to a department.
        # -------------------------------------------------

        if role in (
            UserRole.CITIZEN,
            UserRole.ADMIN,
        ):
            if user_data.department_id is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Citizen and admin users cannot "
                        "be assigned to a department."
                    ),
                )

        # -------------------------------------------------
        # Update User
        # -------------------------------------------------

        user.full_name = user_data.full_name
        user.phone = user_data.phone
        user.role = role.value
        user.department_id = user_data.department_id
        user.is_active = user_data.is_active

        # -------------------------------------------------
        # Save Changes
        # -------------------------------------------------

        db.commit()
        db.refresh(user)

        return user

    # =====================================================
    # Delete User / Soft Delete
    # =====================================================

    @staticmethod
    def delete_user(
        db: Session,
        user_id: int,
    ):
        user = (
            db.query(User)
            .filter(
                User.id == user_id,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        # -------------------------------------------------
        # Prevent Multiple Deactivations
        # -------------------------------------------------

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already deactivated.",
            )

        # -------------------------------------------------
        # Soft Delete
        # -------------------------------------------------

        user.is_active = False

        db.commit()
        db.refresh(user)

        return {
            "message": "User deactivated successfully."
        }