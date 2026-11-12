from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import String,func, DateTime, ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base

class Employees(Base):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, unique=True)
    employee_code: Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
    first_name: Mapped[str] = mapped_column(String(100),nullable=False)
    last_name: Mapped[str] = mapped_column(String(100),nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20),nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(Date,nullable=True)
    gender: Mapped[str | None] = mapped_column(String(10),nullable=True)
    date_of_joining: Mapped[date] = mapped_column(Date,nullable=False)
    department_id:Mapped[int] = mapped_column(ForeignKey('departments.id'), nullable=False)
    manager_id:Mapped[int | None] = mapped_column(ForeignKey('employees.id'), nullable=True)
    annual_leave_balance: Mapped[Decimal] = mapped_column(Numeric(5,2),nullable=False,default=Decimal("12.00"))
    sick_leave_balance: Mapped[Decimal] = mapped_column(Numeric(5,2),nullable=False,default=Decimal("6.00"))
    casual_leave_balance: Mapped[Decimal] = mapped_column(Numeric(5,2),nullable=False,default=Decimal("6.00"))
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())