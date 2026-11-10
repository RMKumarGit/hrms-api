from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator, ConfigDict

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
    status:str
    manager_comments: str | None = Field(default=None,max_length=500)

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

    model_config = ConfigDict(from_attributes=True)
