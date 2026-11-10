from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from src.database.db import get_db
from src.core.security import decode_access_token
from src.models.user import Users

import jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='api/v1/auth/login'
)

security = HTTPBearer()

def get_current_user(
    credentials:Annotated[HTTPAuthorizationCredentials,Depends(security)],
    db:Annotated[Session,Depends(get_db)]
) -> Users:
    token = credentials.credentials
    
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = decode_access_token(token=token)
        subject = payload.get('sub')

        if subject is None:
            raise credential_exception

        user_id = int(subject)
        
    except (jwt.InvalidTokenError, ValueError):
        raise credential_exception

    user = db.get(Users,user_id)

    if user is None or not user.is_active:
        raise credential_exception

    return user