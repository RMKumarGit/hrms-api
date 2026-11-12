from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class DepartmentCreate(BaseModel):
    name: str = Field(min_length=3,max_length=100)
    description: str | None = None

class DepartmentUpdate(BaseModel):
    name: str = Field(min_length=3,max_length=100)
    description:str | None = None
    is_active:bool

class DepartmentResponse(BaseModel):
    id: int
    name: str
    description:str
    is_active:bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)