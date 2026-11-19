from datetime import timedelta, UTC, datetime
from typing import Annotated

from app.core.client import redis_client
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.register import RegisterSchema, RegisterResponseSchema
from app.core.security import get_password_hash, verify_password, create_access_token
from app.dependencies.session import get_db
from app.schemas.token import TokenResponseSchema, AccessTokenResponseSchema, RefreshTokenRequestSchema
from app.core.config import Settings
from app.core.security import create_refresh_token, decode_refresh_token
from app.dependencies.auth import get_current_user

router = APIRouter()

settings = Settings()

#------------------------------------endpoint for registration-------------------------------------
@router.post("/register/",
             response_model=RegisterResponseSchema,
             status_code=status.HTTP_201_CREATED)
def register(
        user_data: RegisterSchema,
        db: Session = Depends(get_db)):  # my DB session injection

    #Check if user with this email already exists
    existing_user = db.execute(select(User).where(User.username == user_data.username))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="username already taken",
                )

    # Hash the password and check if it is valid using my security.py functions
    hashed_password = get_password_hash(user_data.password)

    #Create the database model instance (excluding repeat_password)
    new_user = User(
        name=user_data.name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        birthday=user_data.birthday,
    )

    # Save to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#------------------------------------endpoint for login-------------------------------------
@router.post("/token",
            response_model=TokenResponseSchema,
            status_code=status.HTTP_200_OK)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
          db: Annotated[Session, Depends(get_db)]
          ):
    user = db.execute(select(User).where(User.username == form_data.username)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    is_password_correct = verify_password(form_data.password, user.password)
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires)
    return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token,token_type="bearer")


#-----------------------------------access token validation router----------------------

@router.get("/me",
            response_model=RegisterResponseSchema,
            status_code=status.HTTP_200_OK
            )
def get_me(current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


#-----------------------------------logout router (Through Redis blacklisting)----------------------

@router.post("/logout",
             status_code=status.HTTP_200_OK)
def logout(body: RefreshTokenRequestSchema):
    payload = decode_refresh_token(body.refresh_token)
    current_timestamp = int(datetime.now(UTC).timestamp())
    seconds_left = payload["exp"] - current_timestamp
    if seconds_left > 0:
        redis_client.setex(f"blacklist:{payload['jti']}", seconds_left, "revoked")

    return {"detail":"successfully logged out"}



#-----------------------------------refresh router----------------------
@router.post("/refresh",
            response_model=AccessTokenResponseSchema,)
def refresh(body: RefreshTokenRequestSchema, db:Annotated[Session, Depends(get_db)]):
    payload = decode_refresh_token(body.refresh_token)
    if redis_client.exists(f"blacklist:{payload['jti']}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "type": "access"},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return AccessTokenResponseSchema(access_token=access_token, token_type="bearer")





