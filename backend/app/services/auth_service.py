from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import hash_password


class AuthService:
    """
    Business logic for authentication.
    """

    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user.
        """

        # Check if email already exists
        existing_email = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_email:
            raise ValueError("Email already registered.")

        # Check if phone already exists
        existing_phone = (
            db.query(User)
            .filter(User.phone == user_data.phone)
            .first()
        )

        if existing_phone:
            raise ValueError("Phone number already registered.")

        # Create new user
        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password=hash_password(user_data.password),
            role=user_data.role,
            is_active=True,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user