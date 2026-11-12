from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,status

from src.models.leave_types import LeaveTypes
from src.schemas.leave_types import LeaveTypeCreate, UpdateLeaveType
from src.repositories.leave_type_repository import LeaveTypesRepository

class LeaveTypeService:
    def __init__(self,db:Session):
        self.db = db
        self.leave_type_repository = LeaveTypesRepository(db)

    def create_leave_type(self,data:LeaveTypeCreate) -> LeaveTypes:

        name = data.name.strip()
        code = data.code.strip().upper()

        if not name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Leave Type name cannot be empty"
            )

        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Leave Type code cannot be empty"
            )

        existing_leave_type = self.leave_type_repository.get_by_code(code)

        if existing_leave_type:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Leave type code is already exists'
            )

        leave_type = LeaveTypes(
            name=name,
            code=code,
            description=data.description,
            is_paid=data.is_paid
        )

        try:
            result = self.leave_type_repository.create_leave_types(leave_type)

            self.db.commit()
            self.db.refresh(result)

            return result
        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Leave type already exists"
            )

        except Exception:
            self.db.rollback()
            raise

    def update_leave_types(self, leave_type_id:int,data:UpdateLeaveType) -> LeaveTypes:

        leave_type = self.leave_type_repository.get_by_id(leave_type_id)

        if leave_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Leave type is not found'
            )

        name = data.name.strip()
        
        if not name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Leave type name cannot be empty'
        )

        leave_type.name = name
        leave_type.description = data.description
        leave_type.is_active = data.is_active
        leave_type.is_paid = data.is_paid

        try:
            result = self.leave_type_repository.update_leave_type(leave_type)
            self.db.commit()
            self.db.refresh(result)

            return result
        
        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Unable to update leave type due to duplicate or invalid data"
            )

        except Exception:
            self.db.rollback()
            raise


    def get_leave_types(self) -> list[LeaveTypes]:
        return self.leave_type_repository.get_leave_types()
