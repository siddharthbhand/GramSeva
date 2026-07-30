from sqlalchemy import Column, String, Boolean

from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    full_name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    phone = Column(String(15), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(30), nullable=False)

    is_active = Column(Boolean, default=True)