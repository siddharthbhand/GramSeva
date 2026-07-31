from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User


class UserService:

    @staticmethod
    def get_all_users(db: Session):
        """
        Get all users.
        """
        return (
            db.query(User)
            .order_by(User.id)
            .all()
        )

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """
        Get a user by ID.
        """
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        return user