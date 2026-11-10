from enum import Enum

class UserRole(str, Enum):
    HR_ADMIN = "HR_ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

class LeaveStatus(str, Enum):
    PEDNING = "PEDNING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"