from datetime import date

from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict

class EmployeeCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=2,max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    employee_code: str = Field(min_length=3, max_length=20)
    phone: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    date_of_joining: date
    department_id: int
    manager_id: int | None = None

    @model_validator(mode='after')
    def joining_date_validation(self):
        if self.date_of_joining > date.today():
            raise ValueError('Joining date cannot be in the future')
        return self

class EmployeeResponse(BaseModel):
    email:EmailStr
    first_name: str
    last_name: str
    employee_code: str
    date_of_joining: date
    department_id: int
    manager_id: int | None

    model_config = ConfigDict(from_attributes=True)
