from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.controllers.auth_controller import AuthController
from src.api.dependencies import get_current_user

from src.schemas.user import UserCreate,UserLogin,UserResponse,TokenResponse

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/register',response_model=UserResponse,status_code=201)
def register(data:UserCreate,db:Annotated[Session,Depends(get_db)]):
    controller = AuthController(db)
    return controller.register(data)

@router.post('/login',response_model=TokenResponse,status_code=200)
def login(data:UserLogin,db:Annotated[Session,Depends(get_db)]):
    controller = AuthController(db)
    return controller.login(data)

@router.get('/me',response_model=UserResponse)
def get_me(current_user:Annotated[Session,Depends(get_current_user)]):
    return current_user