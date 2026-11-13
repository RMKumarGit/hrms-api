
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.departments import Departments
from src.schemas.departments import DepartmentCreate, DepartmentUpdate
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

    def update_department(
        self,
        department_id: int,
        data: DepartmentUpdate
    ):
        department = self.db.query(Departments).filter(Departments.id == department_id).first()

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        update_data = data.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing_department = self.repository.get_by_name(
                update_data["name"],
                exclude_id=department_id
            )

            if existing_department:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Department name already exists"
                )

        try:

            result = self.repository.update(
                department,
                update_data
            )

            self.db.commit()
            self.db.refresh(result)

            return result

        except Exception:
            self.db.rollback()
            raise

    def delete_department(self, department_id: int):
        department = self.repository.get_by_id(department_id)

        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        if self.repository.has_employees(department_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You cannot delete department because employees are assigned to it"
            )

        try:
            self.repository.delete(department)
            self.db.commit()

            return {"message": "Department deleted successfully"}

        except Exception:
            self.db.rollback()
            raise
