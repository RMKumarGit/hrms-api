from sqlalchemy.orm import Session

from src.models.departments import Departments
from src.models.employees import Employees


class DepartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str, exclude_id: int | None = None):
        query = self.db.query(Departments).filter(Departments.name == name)

        if exclude_id is not None:
            query = query.filter(Departments.id != exclude_id)

        return query.first()

    def get_by_id(self, id: int):
        return self.db.query(Departments).filter(Departments.id == id).first()

    def create(self, department: Departments):
        self.db.add(department)
        self.db.flush()
        self.db.refresh(department)

        return department

    def get_all(self):
        return self.db.query(Departments).all()

    def update(self, department: Departments, update_data: dict):
        for field, value in update_data.items():
            setattr(department, field, value)
        self.db.add(department)
        return department

    def has_employees(self, department_id: int) -> bool:
        return (
            self.db.query(Employees)
            .filter(Employees.department_id == department_id)
            .first()
            is not None
        )

    def delete(self, department: Departments):
        self.db.delete(department)
