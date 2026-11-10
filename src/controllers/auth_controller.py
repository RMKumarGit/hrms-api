from sqlalchemy.orm import Session
from src.services.auth_service import AuthService
from src.schemas.user import UserLogin,UserCreate,UserResponse, TokenResponse

class AuthController:
    def __init__(self,db:Session):
        self.auth_service = AuthService(db)

    def register(self,data=UserCreate) -> UserResponse:
        user = self.auth_service.register_user(data)
        return UserResponse.model_validate(user)

    def login(self,data=UserLogin) -> TokenResponse:
        result = self.auth_service.login_user(data)
        return TokenResponse.model_validate(result)