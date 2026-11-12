from fastapi import APIRouter
from src.api.v1.auth.router import router as auth_router
from src.api.v1.dept.router import router as dept_router
from src.api.v1.test_permission import router as test_router
from src.api.v1.employee.router import router as employee_router
from src.api.v1.leave_type.router import router as leave_type_router
from src.api.v1.leave_request.router import router as leave_request_router

router = APIRouter(
    prefix='/api/v1'
)

router.include_router(auth_router)
router.include_router(dept_router)
router.include_router(test_router)
router.include_router(employee_router)
router.include_router(leave_type_router)
router.include_router(leave_request_router)