from sqlalchemy.orm import Session
from src.models.user import Users

class UserRepository:
    def __init__(self,db:Session):
        self.db = db

    def get_by_email(self,email:str) -> Users | None:
        return self.db.query(Users).filter(Users.email == email).first()

    def get_by_user_id(self,user_id:int) -> Users | None:
        return self.db.get(Users,user_id)

    def create_user(self,email:str,password:str)-> Users:
        user = Users(
            email = email,
            password_hash = password
        )

        self.db.add(user)
        self.db.flush()

        return user
        