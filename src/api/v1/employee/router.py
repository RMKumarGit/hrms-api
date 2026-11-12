
from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.api.permission import require_roles
from src.models._enum import UserRole
from src.models.user import Users
from src.controllers.employee_controller import EmployeeController
from src.schemas.employees import (
    EmployeeCreate,
    EmployeeResponse,
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.post(
    "/create",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    data: EmployeeCreate,
    db: Annotated[Session, Depends(get_db)],
    curr_user: Users = Depends(
        require_roles(UserRole.HR_ADMIN)
    ),
):
    controller = EmployeeController(db)

    return controller.create_employee(data)


@router.get(
    "/",
    response_model=list[EmployeeResponse],
    status_code=status.HTTP_200_OK
)
def get_employees(
    curr_user: Users = Depends(
        require_roles(
            UserRole.HR_ADMIN,
            UserRole.MANAGER
        )
    ),
    db: Annotated[Session, Depends(get_db)] = None,
):
    controller = EmployeeController(db)

    return controller.get_employees(curr_user)