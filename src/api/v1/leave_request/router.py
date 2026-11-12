from sqlalchemy.orm import Session
from fastapi import APIRouter,status, Depends
from src.database.db import get_db
from src.api.permission import require_roles
from src.models._enum import UserRole

from src.controllers.leave_request_controller import LeaveRequestController
from src.schemas.leave_requests import LeaveRequestCreate, LeaveRequestReview,LeaveRequestResponse

router = APIRouter(
    prefix='/leave-request',
    tags=['Leave Request']
)

@router.post('/create',response_model=LeaveRequestResponse,status_code=status.HTTP_201_CREATED)
def create_leave_request(
    data:LeaveRequestCreate,
    db:Session = Depends(get_db),
    curr_user:Session = Depends(require_roles(UserRole.EMPLOYEE))
):
    controller = LeaveRequestController(db)
    return controller.create_leave_request(curr_user,data)

@router.patch('/{leave_request_id}/review',response_model=LeaveRequestResponse,status_code=status.HTTP_200_OK)
def review_leave_request(
    leave_request_id:int,
    data:LeaveRequestReview,
    db:Session=Depends(get_db),
    curr_user:Session=Depends(require_roles(UserRole.HR_ADMIN,UserRole.MANAGER))
):
    controller = LeaveRequestController(db)
    return controller.review_leave_request(curr_user,leave_request_id,data)
