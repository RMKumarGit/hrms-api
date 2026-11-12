from pydantic import BaseModel, Field, ConfigDict

class LeaveTypeCreate(BaseModel):
    name: str = Field(min_length=3,max_length=20)
    code: str = Field(min_length=3,max_length=20)
    description: str | None = Field(default=None, max_length=1000)
    is_paid: bool

class UpdateLeaveType(BaseModel):
    name: str = Field(min_length=3,max_length=20)
    description: str | None = None
    is_paid:bool
    is_active:bool

class LeaveTypeResponse(BaseModel):
    id: int
    name: str
    code: str
    description: str | None
    is_paid:bool
    is_active:bool

    model_config = ConfigDict(from_attributes=True)
