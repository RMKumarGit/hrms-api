from sqlalchemy import String,text,Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base

class LeaveTypes(Base):
    __tablename__ = 'leave_types'

#     Name	Code	Paid
# Annual Leave	ANNUAL	Yes
# Sick Leave	SICK	Yes
# Casual Leave	CASUAL	Yes
# Unpaid Leave	UNPAID	No

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20),nullable=False)
    code: Mapped[str] = mapped_column(String(20),nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_paid:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text('True'))
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text('True'))
