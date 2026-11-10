from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.db import create_tables
from src.api.v1.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title='HR & Leave Management System',docs_url='/hrms', lifespan=lifespan)


@app.get('/')
def root()->dict[str,str]:
    return dict(message='Welcome to the HR & Leave Management app')


@app.get("/health")
def health()->dict[str,str]:
    return dict(message=f"{__name__} is running successfully")

app.include_router(router)