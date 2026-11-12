from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate, UserLogin
from src.models.user import Users
from src.core.security import hash_password, verify_hash_password, create_access_token

class AuthService:
    def __init__(self,db:Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register_user(self,data:UserCreate)->Users:
        existing_user = self.user_repository.get_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already exists"
            )

        passwod_hash = hash_password(data.password)

        try:
            user = self.user_repository.create_user(email=data.email,password=passwod_hash)

            self.db.commit()
            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise

    def login_user(self,data:UserLogin) -> dict:
        user = self.user_repository.get_by_email(email=data.email)
        print(data)
        print(user)

        if user is None or not verify_hash_password(data.password,user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email or password is invalid",
                headers={"WWW-Authenticate":"Bearer"}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is inactive"
            )

        access_token = create_access_token(user_id=user.id,email=user.email,role=user.role)

        return {
            "email":user.email,
            "access_token":access_token,
            "token_type":"Bearer"
        }