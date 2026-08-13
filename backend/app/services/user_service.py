from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate


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
        # Update User
        # -------------------------------------------------

        user.full_name = user_data.full_name

        user.phone = user_data.phone

        user.role = user_data.role.value

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