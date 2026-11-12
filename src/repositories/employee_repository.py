from sqlalchemy.orm import Session

from src.models.employees import Employees

class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int):
        return (
            self.db.query(Employees)
            .filter(Employees.user_id == user_id)
            .first()
        )

    def get_by_employee_code(self, employee_code: str):
        return self.db.query(Employees).filter(Employees.employee_code == employee_code).first()

    def create(self, employee: Employees):
        self.db.add(employee)
        self.db.flush()
        self.db.refresh(employee)

        return employee

    def get_all(self):
        return self.db.query(Employees).order_by(Employees.id.desc()).all()

    def get_by_manager_id(self, manager_id: int):
        return self.db.query(Employees).filter(Employees.manager_id == manager_id).order_by(Employees.id.desc()).all()
