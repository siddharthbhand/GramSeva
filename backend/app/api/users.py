from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.roles import require_admin
from app.schemas.user import UserListResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=list[UserListResponse],
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return UserService.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserListResponse,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return UserService.get_user_by_id(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserListResponse,
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return UserService.update_user(
        db=db,
        user_id=user_id,
        user_data=user_data,
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return UserService.delete_user(
        db=db,
        user_id=user_id,
    )