from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import String,func, DateTime, ForeignKey, Date, Numeric, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from src.models._enum import LeaveStatus

from src.database.base import Base

class LeaveRequests(Base):
    __tablename__ = 'leave_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey('employees.id'))
    leave_type_id: Mapped[int] = mapped_column(ForeignKey('leave_types.id'))
    start_date: Mapped[date] = mapped_column(Date,nullable=False)
    end_date: Mapped[date] = mapped_column(Date,nullable=False)
    total_days: Mapped[Decimal] = mapped_column(Numeric(5,2),nullable=False)
    reason: Mapped[str] = mapped_column(String(500),nullable=False)
    status: Mapped[LeaveStatus] = mapped_column(SQLAlchemyEnum(LeaveStatus),nullable=False)
    manager_comments: Mapped[str | None] = mapped_column(String(1000),nullable=True)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey('employees.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )