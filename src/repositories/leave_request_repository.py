from sqlalchemy.orm import Session
from src.models.leave_requests import LeaveRequests
from src.models.leave_types import LeaveTypes
from src.models.employees import Employees

class LeaveRequestRepository:
    def __init__(self,db:Session):
        self.db = db

    def get_employee_by_user_id(self,user_id:int):
        return self.db.query(Employees).filter(Employees.user_id == user_id).first()

    def get_employee_by_id_for_update(self,employee_id:int):
        return self.db.query(Employees).filter(Employees.id == employee_id).with_for_update().first()

    def get_leave_type_by_id(self,leave_type_id:int):
        return self.db.get(LeaveTypes,leave_type_id)

    def get_active_leave_type_id(self, leave_type_id:int):
        return self.db.query(LeaveTypes).filter(LeaveTypes.id == leave_type_id,LeaveTypes.is_active.is_(True)).first()

    def create_leave_request(self,data:LeaveRequests):
        self.db.add(data)
        self.db.flush()
        self.db.refresh(data)
        return data

    def get_by_id_for_update(self,leave_request_id:int):
        return self.db.query(LeaveRequests).filter(LeaveRequests.id == leave_request_id).with_for_update().first()
        
    