from datetime import datetime

from sqlalchemy import String, func,text,Boolean, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column
from src.models._enum import UserRole
from src.database.base import Base

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(225), nullable=False,unique=True)
    password_hash:Mapped[str] = mapped_column(String(255),nullable=False)
    role:Mapped[UserRole] = mapped_column(SQLAlchemyEnum(UserRole), nullable=True, default=UserRole.EMPLOYEE,server_default=text('EMPLOYEE'))
    is_active:Mapped[bool] = mapped_column(Boolean, nullable=True, default=True, server_default=text('True'))
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())