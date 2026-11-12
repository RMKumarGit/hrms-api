from sqlalchemy.orm import Session
from src.models.leave_types import LeaveTypes

class LeaveTypesRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_code(self,code:str)->LeaveTypes | None:
        return self.db.query(LeaveTypes).filter(LeaveTypes.code == code).first()

    def get_by_id(self,id:int)->LeaveTypes | None:
        return self.db.get(LeaveTypes,id)

    def create_leave_types(self, data:LeaveTypes) -> LeaveTypes:
        self.db.add(data)
        self.db.flush()

        self.db.refresh(data)

        return data

    def update_leave_type(self,data:LeaveTypes) -> LeaveTypes:
        self.db.flush()
        self.db.refresh(data)

        return data

    def get_leave_types(self) -> list[LeaveTypes]:
        return self.db.query(LeaveTypes).filter(LeaveTypes.is_active.is_(True)).order_by(LeaveTypes.id.asc()).all()
