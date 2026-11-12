from sqlalchemy.orm import Session

from src.models.departments import Departments


class DepartmentRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str):
        return self.db.query(Departments).filter(Departments.name == name).first()

    def create(self, department: Departments):
        self.db.add(department)
        self.db.flush()
        self.db.refresh(department)

        return department

    def get_all(self):
        return self.db.query(Departments).all()
