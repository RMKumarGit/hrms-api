from src.services.department_service import DepartmentService
from src.schemas.departments import (
    DepartmentCreate,
    DepartmentResponse,
)


class DepartmentController:

    def __init__(self, db):
        self.department_service = DepartmentService(db)

    def create_department(
        self,
        data: DepartmentCreate
    ) -> DepartmentResponse:

        department = self.department_service.create_department(data)

        return DepartmentResponse.model_validate(department)

    def get_all_departments(self) -> list[DepartmentResponse]:

        departments = self.department_service.get_all_departments()

        return [
            DepartmentResponse.model_validate(dept)
            for dept in departments
        ]