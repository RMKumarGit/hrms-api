from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, ConfigDict
from src.models._enum import LeaveStatus

class LeaveRequestCreate(BaseModel):
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str = Field(min_length=5,max_length=500)

    @model_validator(mode='after')
    def date_validation(self):
        if self.start_date > self.end_date:
            raise ValueError('End date cannot be before start date')
        return self

class LeaveRequestReview(BaseModel):
    status:LeaveStatus
    manager_comments: str | None = Field(default=None,max_length=500)

    @model_validator(mode='after')
    def review_validation(self):
        if self.status not in (LeaveStatus.APPROVED,LeaveStatus.REJECTED):
            raise ValueError('Review status must be APPROVED or REJECTED')
        if self.manager_comments is not None:
            self.manager_comments = self.manager_comments.strip() or None

        return self

class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    total_days: Decimal
    reason: str
    status: str
    manager_comments: str | None
    created_at: datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)
