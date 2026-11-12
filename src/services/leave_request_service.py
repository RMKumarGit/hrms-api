
from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.employees import Employees
from src.models.leave_requests import LeaveRequests
from src.models._enum import LeaveStatus, UserRole
from src.repositories.leave_request_repository import LeaveRequestRepository


class LeaveRequestService:

    def __init__(self, db: Session):
        self.db = db
        self.leave_request_repository = LeaveRequestRepository(db)

    BALANCE_FIELDS = {
        "ANNUAL": "annual_leave_balance",
        "SICK": "sick_leave_balance",
        "CASUAL": "casual_leave_balance",
    }

    def _get_balance_field(self, leave_type):
        if not leave_type.is_paid:
            return None

        balance_field = self.BALANCE_FIELDS.get(leave_type.code)

        if not balance_field:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Balance mapping is not configured for this leave type"
            )

        return balance_field

    def create_leave_request(self, curr_user, data):

        employee = self.leave_request_repository.get_employee_by_user_id(
            curr_user.id
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee profile not found"
            )

        leave_type = self.leave_request_repository.get_active_leave_type_id(
            data.leave_type_id
        )

        if not leave_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active leave type not found"
            )

        if data.start_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Leave cannot be applied for past dates"
            )

        total_days = Decimal(
            (data.end_date - data.start_date).days + 1
        )

        balance_field = self._get_balance_field(leave_type)

        if balance_field:
            available_balance = getattr(employee, balance_field)

            if available_balance < total_days:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient leave balance"
                )

        leave_request = LeaveRequests(
            employee_id=employee.id,
            leave_type_id=leave_type.id,
            start_date=data.start_date,
            end_date=data.end_date,
            total_days=total_days,
            reason=data.reason,
            status=LeaveStatus.PENDING,
            manager_comments=None,
            approved_by=None,
        )

        try:
            self.leave_request_repository.create_leave_request(leave_request)
            self.db.commit()
            self.db.refresh(leave_request)

            return leave_request

        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Unable to create leave request"
            )

        except Exception:
            self.db.rollback()
            raise

    def review_leave_request(self, curr_user, leave_request_id: int, data):

        leave_request = (
            self.leave_request_repository.get_by_id_for_update(
                leave_request_id
            )
        )

        if not leave_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave request not found"
            )

        if leave_request.status != LeaveStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending leave requests can be reviewed"
            )

        employee = self.leave_request_repository.get_employee_by_id_for_update(
            leave_request.employee_id
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee profile not found"
            )

        if employee.user_id == curr_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot review your own leave request"
            )

        if curr_user.role == UserRole.HR_ADMIN:
            pass

        elif curr_user.role == UserRole.MANAGER:

            manager = self.leave_request_repository.get_employee_by_user_id(
                curr_user.id
            )

            if not manager:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Manager employee profile not found"
                )

            if employee.manager_id != manager.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can review only your direct reports' requests"
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to review leave requests"
            )

        leave_type = self.leave_request_repository.get_leave_type_by_id(
            leave_request.leave_type_id
        )

        if not leave_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Leave type not found"
            )

        try:
            if data.status == LeaveStatus.APPROVED:

                balance_field = self._get_balance_field(leave_type)

                if balance_field:
                    available_balance = getattr(employee, balance_field)

                    if available_balance < leave_request.total_days:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Insufficient leave balance to approve this request"
                        )

                    setattr(
                        employee,
                        balance_field,
                        available_balance - leave_request.total_days
                    )

            leave_request.status = data.status
            leave_request.manager_comments = data.manager_comments
            leave_request.approved_by = curr_user.id

            self.db.commit()
            self.db.refresh(leave_request)

            return leave_request

        except Exception:
            self.db.rollback()
            raise
