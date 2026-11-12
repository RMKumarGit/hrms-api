from src.services.leave_type_service import LeaveTypeService

from src.schemas.leave_types import LeaveTypeCreate, LeaveTypeResponse, UpdateLeaveType

class LeaveTypeController:

    def __init__(self,db):
        self.leave_type_service = LeaveTypeService(db)

    def create_leave_type(self,data:LeaveTypeCreate) -> LeaveTypeResponse:
        leave_type = self.leave_type_service.create_leave_type(data)

        return LeaveTypeResponse.model_validate(leave_type)

    def update_leave_type(self,leave_type_id:int,data:UpdateLeaveType) -> LeaveTypeResponse:
        leave_type = self.leave_type_service.update_leave_types(leave_type_id,data)

        return LeaveTypeResponse.model_validate(leave_type)

    def get_leave_types(self) -> list[LeaveTypeResponse]:
        leave_types = self.leave_type_service.get_leave_types()

        return [
            LeaveTypeResponse.model_validate(leave_type)
            for leave_type in leave_types
        ]
