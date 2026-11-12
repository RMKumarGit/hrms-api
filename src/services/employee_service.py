
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.user import Users
from src.models.employees import Employees
from src.models.departments import Departments
from src.models._enum import UserRole

from src.repositories.employee_repository import EmployeeRepository


class EmployeeService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = EmployeeRepository(db)

    def create_employee(self, data: Employees) -> Employees:

        employee_code = data.employee_code.strip()

        if not employee_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee code cannot be empty"
            )

        user = self.db.get(Users, data.user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=400,
                detail="User account is inactive"
            )

        if user.role not in (UserRole.EMPLOYEE, UserRole.MANAGER):
            raise HTTPException(
                status_code=400,
                detail="Only Employee or Manager accounts can have employee profiles"
            )

        existing_user = self.repository.get_by_user_id(
            data.user_id
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee profile already exists for this user"
            )

        existing_code = self.repository.get_by_employee_code(
            employee_code
        )

        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee code already exists"
            )

        department = self.db.get(
            Departments,
            data.department_id
        )

        if department is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        if not department.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign employee to an inactive department"
            )

        if data.manager_id is not None:

            manager = self.db.get(
                Employees,
                data.manager_id
            )

            if manager is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Manager not found"
                )

        employee = Employees(
            user_id=data.user_id,
            employee_code=employee_code,
            first_name=data.first_name.strip(),
            last_name=data.last_name.strip(),
            phone=data.phone,
            date_of_birth=data.date_of_birth,
            gender=data.gender,
            date_of_joining=data.date_of_joining,
            department_id=data.department_id,
            manager_id=data.manager_id,
        )

        try:
            result = self.repository.create(employee)

            self.db.commit()
            self.db.refresh(result)

            return result

        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=409,
                detail="Employee already exists or referenced data is invalid"
            )

        except Exception:
            self.db.rollback()
            raise

    def get_employees(self, current_user: Users):

        if current_user.role == UserRole.HR_ADMIN:
            return self.repository.get_all()

        if current_user.role == UserRole.MANAGER:

            manager = self.repository.get_by_user_id(
                current_user.id
            )

            if manager is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Manager employee profile not found"
                )

            return self.repository.get_by_manager_id(
                manager.id
            )

        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view employees"
        )
