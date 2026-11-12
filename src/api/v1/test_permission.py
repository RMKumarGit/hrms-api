from fastapi import Depends, APIRouter
from src.api.dependencies import get_current_user
from src.models.user import Users
from src.api.permission import require_roles
from src.models._enum import UserRole

router = APIRouter(prefix='/permission',tags=['Permission'])

@router.get('/admin')
def admin_only(curr_user:Users = Depends(require_roles(UserRole.HR_ADMIN))):
    return {
        "message":"Welcome HR Admin",
        "user_id":curr_user.id,
        "user_email":curr_user.email
    }

@router.get('/manager')
def admin_or_manager(curr_user:Users = Depends(require_roles(UserRole.HR_ADMIN,UserRole.MANAGER))):
    return {
        "message":"Welcome Manager or HR Admin",
        "user_id":curr_user.id,
        "user_email":curr_user.email
    }

@router.get('/authendicated')
def authendicated_user(curr_user:Users = Depends(require_roles(UserRole.EMPLOYEE,UserRole.HR_ADMIN,UserRole.MANAGER))):
    return {
        "message":"Welcome",
        "user_id":curr_user.id,
        "user_email":curr_user.email
    }
