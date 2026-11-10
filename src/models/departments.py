from datetime import datetime

from sqlalchemy import String,func,text,Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base

class Departments(Base):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20),nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('False'))
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())