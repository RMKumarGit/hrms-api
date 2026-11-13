from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator

class DepartmentCreate(BaseModel):
    name: str = Field(min_length=3,max_length=100)
    description: str | None = None

class DepartmentUpdate(BaseModel):
    name: str = Field(min_length=3,max_length=100)
    description:str | None = Field(default=None, max_length=1000)
    is_active:bool

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("At least one field is required")

        if "name" in self.model_fields_set and self.name is None:
            raise ValueError("Department name cannot be null")

        if "is_active" in self.model_fields_set and self.is_active is None:
            raise ValueError("is_active cannot be null")

        return self

class DepartmentResponse(BaseModel):
    id: int
    name: str
    description:str
    is_active:bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)