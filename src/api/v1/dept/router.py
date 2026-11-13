from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.permission import require_roles
from src.models._enum import UserRole
from src.models.user import Users
from src.database.db import get_db

from src.controllers.department_controller import DepartmentController
from src.schemas.departments import DepartmentCreate, DepartmentResponse, DepartmentUpdate


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "/create",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    payload: DepartmentCreate,
    db: Annotated[Session, Depends(get_db)],
    curr_user: Users = Depends(
        require_roles(UserRole.HR_ADMIN)
    ),
):
    controller = DepartmentController(db)
    return controller.create_department(payload)


@router.get(
    "/",
    response_model=list[DepartmentResponse],
    status_code=status.HTTP_200_OK
)
def get_departments(
    curr_user: Annotated[Users, Depends(
        require_roles(UserRole.HR_ADMIN)
    )],
    db: Annotated[Session, Depends(get_db)]
):
    controller = DepartmentController(db)
    return controller.get_all_departments()

@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK
)
def update_department(
    department_id:int,
    data:DepartmentUpdate,
    curr_user: Annotated[Users, Depends(
        require_roles(UserRole.HR_ADMIN)
    )],
    db: Annotated[Session, Depends(get_db)]
):
    controller = DepartmentController(db)
    return controller.update_department(data,department_id)

@router.delete(
    "/{department_id}",
    status_code=status.HTTP_200_OK
)
def delete_department_by_id(
    department_id:int,
    curr_user: Annotated[Users, Depends(
        require_roles(UserRole.HR_ADMIN)
    )],
    db: Annotated[Session, Depends(get_db)]
):
    controller = DepartmentController(db)
    return controller.delete_deparment(department_id)