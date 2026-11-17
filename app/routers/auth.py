from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.register import RegisterSchema, RegisterResponseSchema
from app.core.security import get_password_hash
from app.dependencies.session import get_db

router = APIRouter()


@router.post("/register/",
             response_model=RegisterResponseSchema,
             status_code=status.HTTP_201_CREATED)
def register(
        user_data: RegisterSchema,
        db: Session = Depends(get_db)):  # my DB session injection

    #Check if user with this email already exists
    existing_user = db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                )

    # Hash the password and check if it is valid using my security.py functions
    hashed_password = get_password_hash(user_data.password)

    #Create the database model instance (excluding repeat_password)
    new_user = User(
        name=user_data.name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hashed_password,
        birthday=user_data.birthday,
    )

    # Save to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

