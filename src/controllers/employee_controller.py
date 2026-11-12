
from src.services.employee_service import EmployeeService
from src.schemas.employees import (
    EmployeeCreate,
    EmployeeResponse,
)
from src.models.user import Users

class EmployeeController:

    def __init__(self, db):
        self.employee_service = EmployeeService(db)

    def create_employee(
        self,
        data: EmployeeCreate
    ) -> EmployeeResponse:

        employee = self.employee_service.create_employee(data)

        return EmployeeResponse.model_validate(employee)

    def get_employees(
        self,
        current_user: Users
    ) -> list[EmployeeResponse]:

        employees = self.employee_service.get_employees(
            current_user
        )

        return [
            EmployeeResponse.model_validate(employee)
            for employee in employees
        ]
