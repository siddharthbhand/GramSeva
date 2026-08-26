from typing import Callable

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.core.user_roles import UserRole


def require_admin(
    current_user: User = Depends(get_current_user),
):
    """
    Allow only admin users.
    """

    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admins only.",
        )

    return current_user


def require_role(
    *allowed_roles: UserRole,
) -> Callable:
    """
    Create a dependency that allows one or more roles.
    """

    allowed_values = {
        role.value
        for role in allowed_roles
    }

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.role not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Insufficient permissions.",
            )

        return current_user

    return role_checker