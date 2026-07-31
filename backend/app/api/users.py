from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin
from app.models.user import User
from app.schemas.user import UserListResponse
from app.services.user_service import UserService

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserListResponse],
)
def get_all_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Get all users (Admin only).
    """
    return UserService.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserListResponse,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    """
    Get a user by ID (Admin only).
    """
    return UserService.get_user_by_id(db, user_id)