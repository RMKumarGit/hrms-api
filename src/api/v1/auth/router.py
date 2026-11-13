from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis_fastapi import rate_limit

from src.database.db import get_db
from src.controllers.auth_controller import AuthController
from src.api.dependencies import get_current_user
from src.schemas.user import UserCreate,UserLogin,UserResponse,TokenResponse
from src.core.rate_limit import rate_limit_exceeded_response

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/register',response_model=UserResponse,status_code=201,dependencies=[Depends(rate_limit('4/minute',on_limit_exceeded=rate_limit_exceeded_response))])
def register(data:UserCreate,db:Annotated[Session,Depends(get_db)]):
    controller = AuthController(db)
    return controller.register(data)

@router.post('/login',response_model=TokenResponse,status_code=200,dependencies=[Depends(rate_limit('3/minute',on_limit_exceeded=rate_limit_exceeded_response))])
def login(data:UserLogin,db:Annotated[Session,Depends(get_db)]):
    controller = AuthController(db)
    return controller.login(data)

@router.get('/me',response_model=UserResponse,dependencies=[Depends(rate_limit('5/minute',on_limit_exceeded=rate_limit_exceeded_response))])
def get_me(current_user:Annotated[Session,Depends(get_current_user)]):
    return current_user