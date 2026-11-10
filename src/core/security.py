from datetime import datetime, timedelta, timezone

import jwt

from pwdlib import PasswordHash
from src.core.config import get_settings

settings = get_settings()

password_hash = PasswordHash.recommended()

def hash_password(password:str) -> str:
    return password_hash.hash(password)

def verify_hash_password(plain_password:str,hash_passsword:str) -> bool:
    return password_hash.verify(
        plain_password,
        hash_passsword
    )

def create_access_token(user_id:int,email:str,role:str) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_mins
    )

    payload = {
        "sub":str(user_id),
        "role":role,
        "email":email,
        "exp":expire_at
    }

    return jwt.encode(
        payload=payload,
        algorithm=settings.algorithm,
        key=settings.secret_key
    )

def decode_access_token(token:str):
    return jwt.decode(
        token,
        key=settings.secret_key,
        algorithms=settings.algorithm
    )