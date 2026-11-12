
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.departments import Departments
from src.schemas.departments import DepartmentCreate
from src.repositories.department_repository import DepartmentRepository


class DepartmentService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = DepartmentRepository(db)

    def create_department(self, data:DepartmentCreate) -> Departments:

        name = data.name.strip()

        if not name:
            raise HTTPException(
                status_code=400,
                detail="Department name cannot be empty"
            )

        existing_department = self.repository.get_by_name(name)

        if existing_department:
            raise HTTPException(
                status_code=409,
                detail="Department already exists"
            )

        department = Departments(
            name=name,
            description=data.description,
        )

        try:
            result = self.repository.create(department)

            self.db.commit()
            self.db.refresh(result)

            return result

        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=409,
                detail="Department already exists"
            )

        except Exception:
            self.db.rollback()
            raise

    def get_all_departments(self) -> list[Departments]:

        return self.repository.get_all() 
