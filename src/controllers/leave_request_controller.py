from src.services.leave_request_service import LeaveRequestService
from src.schemas.leave_requests import LeaveRequestCreate, LeaveRequestReview, LeaveRequestResponse

class LeaveRequestController:
    def __init__(self,db):
        self.leave_request_service = LeaveRequestService(db)

    def create_leave_request(self,curr_user,data:LeaveRequestCreate) -> LeaveRequestResponse:
        leave_request = self.leave_request_service.create_leave_request(curr_user,data)
        return LeaveRequestResponse.model_validate(leave_request)

    def review_leave_request(self,curr_user,leave_request_id:int,data:LeaveRequestReview) -> LeaveRequestResponse:
        leave_request = self.leave_request_service.review_leave_request(curr_user,leave_request_id,data)
        return LeaveRequestResponse.model_validate(leave_request)