from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import RequestValidationError
from redis_fastapi import FastAPIRedis

from src.api.v1.router import router
from src.core.exception_handlers import http_exception_handler, validation_exception_handler, database_exception_handler, general_exception_handler

app = FastAPI(title='HR & Leave Management System',docs_url='/hrms')


@app.get('/')
def root()->dict[str,str]:
    return dict(message='Welcome to the HR & Leave Management app')


@app.get("/health")
def health()->dict[str,str]:
    return dict(message=f"{__name__} is running successfully")

FastAPIRedis(app).lifespan().rate_limiting()

app.include_router(router)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)