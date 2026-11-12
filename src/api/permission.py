from fastapi import Depends, HTTPException, status

from src.models._enum import UserRole
from src.models.user import Users

from src.api.dependencies import get_current_user

def require_roles(*allowed_roles:UserRole):
    def role_checking(curr_user:Users = Depends(get_current_user)) -> Users:
        if curr_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have the permission to perform this action"
            )

        return curr_user

    return role_checking
 