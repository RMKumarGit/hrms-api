from sqlalchemy.orm import Session
from fastapi import APIRouter,status, Depends
from src.database.db import get_db
from src.models.user import Users
from src.api.permission import require_roles
from src.models._enum import UserRole
from src.api.dependencies import get_current_user

from src.controllers.leave_type_controller import LeaveTypeController
from src.schemas.leave_types import LeaveTypeCreate,LeaveTypeResponse, UpdateLeaveType

router = APIRouter(
    prefix='/leave-type',
    tags=['Leave Type']
)

@router.post('/create',response_model=LeaveTypeCreate, status_code=status.HTTP_201_CREATED)
def create_leave_type(
    data:LeaveTypeCreate,
    db: Session = Depends(get_db),
    curr_user: Users = Depends(require_roles(UserRole.HR_ADMIN))
):
    controller = LeaveTypeController(db)

    return controller.create_leave_type(data)

@router.put('/{leave_type_id}',response_model=LeaveTypeResponse,status_code=status.HTTP_200_OK)
def update_leave_type(
    leave_type_id:int,
    data:UpdateLeaveType,
    db:Session = Depends(get_db),
    curr_user:Users = Depends(require_roles(UserRole.HR_ADMIN))
):
    controller = LeaveTypeController(db)

    return controller.update_leave_type(leave_type_id,data)

@router.get('/',response_model=list[LeaveTypeResponse],status_code=status.HTTP_200_OK)
def get_all_leave_types(
    db: Session = Depends(get_db),
    curr_user: Users = Depends(get_current_user)
):
    controller = LeaveTypeController(db)

    return controller.get_leave_types()