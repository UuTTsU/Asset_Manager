from typing import Annotated
import jwt
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.config import Settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.dependencies.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
settings = Settings()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        if payload.get("type") != "access":
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = db.execute(select(User).where(User.username==username)).scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


