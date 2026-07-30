from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserRegister
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    def register_user(db: Session, user_data: UserRegister):

        existing_email = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_email:
            raise ValueError("Email already registered.")

        existing_phone = (
            db.query(User)
            .filter(User.phone == user_data.phone)
            .first()
        )

        if existing_phone:
            raise ValueError("Phone number already registered.")

        hashed_password = hash_password(user_data.password)

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password=hashed_password,
            role=user_data.role,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user


    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str,
    ):

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            password,
            user.password,
        ):
            raise ValueError("Invalid email or password.")

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